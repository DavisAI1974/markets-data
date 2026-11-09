"""Inference from supplied frozen coefficients; never fits or selects a model."""
import math
from .contract import UNKNOWN,ns,available

def finite_number(x):
    return not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x)

def predict_frozen_linear(model,context,bindings,freeze_ns):
    decision=ns(context['decision_ns'])
    # Caller supplies a verified artifact manifest time, not a training cutoff.
    # At equal ns no artifact ordering proof is available through this helper.
    if ns(freeze_ns)>=decision:return UNKNOWN
    names=model['features'];n=len(names)
    if len(set(names))!=n or len(model['imputation'])!=n or any(len(model[k])!=2*n for k in ['center','scale','coefficients']):
        raise ValueError('Frozen model dimensions are inconsistent')
    if any(not finite_number(v) for k in ['imputation','center','scale','coefficients'] for v in model[k]) or not finite_number(model['intercept']):
        raise ValueError('Frozen model contains nonfinite values')
    if any(x<=0 for x in model['scale']):raise ValueError('Frozen scales must be positive')
    values=[];missing=[]
    for i,name in enumerate(names):
        f=context.get('fields',{}).get(name)
        if not available(f,context):return UNKNOWN
        binding=bindings.get(name)
        if not isinstance(binding,str) or not binding or f.get('definition_id')!=binding:return UNKNOWN
        status=f.get('status');v=f['value']
        if status=='observed_undefined':
            if v is not None:raise ValueError('Observed-undefined must explicitly use null')
            values.append(model['imputation'][i]);missing.append(1)
        elif status=='observed' and finite_number(v):values.append(v);missing.append(0)
        else:return UNKNOWN
    x=values+missing
    result=model['intercept']+sum((v-c)/s*w for v,c,s,w in zip(x,model['center'],model['scale'],model['coefficients']))
    return result if finite_number(result) else UNKNOWN
