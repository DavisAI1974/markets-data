"""Field projections. Preserve source phases and all original S cells."""
import bisect


def latest_ties(rows, cutoff):
    eligible=[r for r in rows if r['known_by_ns']<=cutoff]
    if not eligible:return []
    clock=max(r['known_by_ns'] for r in eligible)
    return [r for r in eligible if r['known_by_ns']==clock]


def lifecycle_projection(events, field):
    actions={'L030':'A','L031':'C','L032':'M','L033':'M','L034':'T','L035':'F','L036':'R'}
    if field in actions:
        return [r for r in events if r['original_message']['action']==actions[field]]
    if field=='L028':
        return [r for r in events if r['original_message'].get('is_snapshot') or r['original_message']['action']=='R']
    return events


def book_projection(book, field):
    if field in ('L041','L042','L043','L044'):
        result={}
        for side in ['bid','ask']:
            levels=[]
            for level in book[side+'_levels_full']:
                v={'price_raw':level['price_raw'],'size':level['size'],'order_count':level['order_count']}
                if field=='L041':v['fifo_queue']=level['fifo_queue']
                if field=='L042':
                    v.update({k:level.get(k) for k in ['front_order_age_s','queue_age_median_s','queue_age_p90_s']})
                    v['orders']=[{k:o.get(k) for k in ['order_id','priority_recv_ns','priority_sequence','priority_age_s']} for o in level['fifo_queue']]
                if field=='L043':
                    v['largest_order_share']=level.get('largest_order_share')
                    v['size_hhi']=sum((o['size']/level['size'])**2 for o in level['fifo_queue']) if level['size'] else None
                if field=='L044':
                    v['orders']=[{k:o.get(k) for k in ['order_id','size','volume_ahead']} for o in level['fifo_queue']]
                levels.append(v)
            result[side]=levels
        return result
    keys={
        'L039':['bid_depth_full','ask_depth_full','bid_levels_full','ask_levels_full'],
        'L040':['bid_price_level_count_full','ask_price_level_count_full','bid_order_count_full','ask_order_count_full'],
        'L045':['best_bid','best_ask','spread','mid','depth_imbalance_full'],
        'L052':['best_bid','best_ask','mid','bid_depth_full','ask_depth_full'],
        'L054':['best_bid','best_ask','mid'],
        'L057':['depth_imbalance_full','bid_depth_full','ask_depth_full'],
    }[field]
    result={k:book[k] for k in keys}
    if field=='L039':
        for side in ['bid','ask']:
            result[side+'_levels_full']=[{k:v for k,v in level.items() if k!='fifo_queue'} for level in book[side+'_levels_full']]
    return result
