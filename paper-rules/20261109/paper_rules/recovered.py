"""Source-bound M0/M1 feature construction and inference. No fitting or routing."""
from bisect import bisect_left, bisect_right
import hashlib
import json
import math
from .contract import UNKNOWN, ns
from .models import _predict_values, finite_number
from .source_information import signed_flow_features

NS = 1_000_000_000
RECOVERY_SHA256='c6b315463845bbb09b94a33f24a2d51dd97499ba2554a2b79546268c7c4fd771'
SOURCE_MANIFEST_SHA256='e1071fd3b91a1cc521832bff1c79bef42aa7aec554ac35906fd3e77137cc9a98'


def verify_recovery(root):
    folder = root/'recovery/model_source_audit'
    manifest_bytes=(folder/'SOURCE_MANIFEST.json').read_bytes()
    recovery_bytes=(folder/'M0M1_BINDING_RECOVERY.json').read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest()!=SOURCE_MANIFEST_SHA256 or hashlib.sha256(recovery_bytes).hexdigest()!=RECOVERY_SHA256:
        raise ValueError('Recovered binding or source manifest differs from reviewed bytes')
    manifest = json.loads(manifest_bytes)
    for source in manifest:
        content = (folder/source['file']).read_bytes()
        blob = b'blob '+str(len(content)).encode()+b'\0'+content
        if hashlib.sha256(content).hexdigest()!=source['sha256'] or hashlib.sha1(blob).hexdigest()!=source['git_blob_sha']:
            raise ValueError('Recovered source hash mismatch: '+source['file'])
    recovery = json.loads(recovery_bytes)
    canonical = json.loads((folder/'canonical_TRADE_RULES.json').read_text())
    definitions={d['id']:d for d in recovery['features']}
    for name, model in recovery['models'].items():
        if model['state']!=canonical['models'][name]:raise ValueError('Frozen state differs from original')
        names=model['state']['features']; ids=model['ordered_feature_definition_ids']
        if len(names)!=len(ids) or any(definitions[d]['name']!=n for n,d in zip(names,ids)):
            raise ValueError('Ordered source feature binding mismatch')
    return recovery


def build_model_context(groups, flow, *, last_closed_second):
    """Consume complete-group observations through recognition and 20 closed bins.

    groups must be a contiguous, time-ordered slice including the quote before
    the flow window and the latest quote at/before recognition minus 20 seconds.
    Caller constructs the causal recognition event; source candidate IDs are
    never accepted as signals. No sparse or failed-feed bin is treated as zero.
    """
    if not groups or len(flow)!=20:return UNKNOWN
    times=[ns(g['receive_ns']) for g in groups]
    cursors=[ns(g['cursor']) for g in groups]
    if any(a>b for a,b in zip(times,times[1:])) or any(a>=b for a,b in zip(cursors,cursors[1:])):
        raise ValueError('Groups must be ordered by receive clock and cursor')
    current=groups[-1]; t=times[-1]; cursor=cursors[-1]
    end=ns(last_closed_second)
    if (end+1)*NS>t:return UNKNOWN
    k=bisect_right(times,t-20*NS)-1
    kflow=bisect_left(times,(end-19)*NS)-1
    if min(k,kflow)<0:return UNKNOWN
    segment=current['segment']
    required=groups[min(k,kflow):]
    indices=[ns(g['group_index']) for g in required]
    if any(b!=a+1 for a,b in zip(indices,indices[1:])):return UNKNOWN
    for g in required:
        if g.get('valid') is not True or g['segment']!=segment:return UNKNOWN
        if any(type(g[key]) is not int for key in ('bid_raw','ask_raw')):return UNKNOWN
        if not (0<g['bid_raw']<g['ask_raw']):return UNKNOWN
        if any(not finite_number(g[key]) or g[key]<0 for key in ('bid_lots','ask_lots','bid_orders','ask_orders')):
            return UNKNOWN
    if [ns(f['second']) for f in flow]!=list(range(end-19,end+1)):return UNKNOWN
    for row in flow:
        if row.get('complete') is not True or row.get('classification')!='previous_completed_group_midpoint':return UNKNOWN
        if row.get('segment')!=segment or ns(row['known_by_ns'])>t or ns(row['known_by_cursor'])>cursor:return UNKNOWN
        if ns(row['known_by_ns'])<(ns(row['second'])+1)*NS:return UNKNOWN
        if any(not finite_number(row[key]) or row[key]<0 for key in ('buy','sell')):return UNKNOWN
    buy=[r['buy'] for r in flow];sell=[r['sell'] for r in flow]
    twice_mid=[g['bid_raw']+g['ask_raw'] for g in groups[k:]]
    b,s=current['bid_lots'],current['ask_lots']
    bo,so=current['bid_orders'],current['ask_orders']
    values=dict(prior_ticks20=(twice_mid[-1]-twice_mid[0])/2e6,
                range_ticks20=(max(twice_mid)-min(twice_mid))/2e6,
                spread_ticks=(current['ask_raw']-current['bid_raw'])/1e6,
                touch_imb=(b-s)/(b+s) if b+s else None,
                touch_count_imb=(bo-so)/(bo+so) if bo+so else None,
                log_touch_lots=math.log1p(b+s), log_touch_orders=math.log1p(bo+so),
                early_buy=sum(buy[:10]),early_sell=sum(sell[:10]),
                late_buy=sum(buy[10:]),late_sell=sum(sell[10:]),
                fresh_buy5=sum(buy[-5:]),fresh_sell5=sum(sell[-5:]))
    information=signed_flow_features(buy,sell)
    for name in ('ent_dipole','mi_flow','imb_flow'):
        values[name]=None if information is None else information[name]
    signed=None if information is None else information['C_signed']
    values['log_signed_C']=None if signed is None else (1 if signed>0 else -1 if signed<0 else 0)*math.log1p(abs(signed))
    return dict(decision_ns=t,decision_cursor=cursor,fields={
        name:dict(value=value,status='observed_undefined' if value is None else 'observed',
                  role='feature',known_by_ns=t,known_by_cursor=cursor,
                  definition_id='source-M0M1-'+name) for name,value in values.items()})


def predict_bound_model(recovery,name,context,*,artifact_available_session_ns,decision_session_ns,session_id):
    """Model availability uses the paper session clock; features use market time.

    Session timestamps must come from the same monotonic session recorder.
    The caller records actual artifact loading; training dates cannot supply it.
    """
    if not isinstance(session_id,str) or not session_id:return UNKNOWN
    if context is UNKNOWN:return UNKNOWN
    if ns(artifact_available_session_ns)>=ns(decision_session_ns):return UNKNOWN
    model=recovery['models'][name]
    bindings=dict(zip(model['state']['features'],model['ordered_feature_definition_ids']))
    return _predict_values(model['state'],context,bindings)
