"""Restricted causal expressions; no order routing and no synthetic fills."""
import math
import re
from functools import reduce
from operator import mul

UNKNOWN=object()
OPS={'and','or','not','eq','ne','gt','ge','lt','le','add','sub','mul','div','abs','sign','in','min','max'}
ARITY={'not':1,'abs':1,'sign':1,'eq':2,'ne':2,'gt':2,'ge':2,'lt':2,'le':2,'sub':2,'div':2,'in':2}

def ns(value):
    if isinstance(value,bool) or not isinstance(value,(int,str)):
        raise ValueError('Nanosecond clocks must be integer or decimal integer text')
    if isinstance(value,str) and not re.fullmatch(r'-?\d+',value):
        raise ValueError('Nanosecond clock is not an exact integer')
    return int(value)

def valid(value):
    if isinstance(value,list):return all(valid(v) for v in value)
    return value is not None and not (isinstance(value,float) and not math.isfinite(value))

def available(field,context):
    if not isinstance(field,dict) or 'value' not in field or 'known_by_ns' not in field:return False
    if field.get('role') not in {'feature','decision_state','execution_state'}:return False
    known=ns(field['known_by_ns']);decision=ns(context['decision_ns'])
    if known>decision:return False
    # Cursors belong to the same monotonically ordered complete-group stream.
    # A timer carries the last consumed cursor, never a fabricated next group.
    cursor=context.get('decision_cursor');field_cursor=field.get('known_by_cursor')
    if cursor is not None:
        if field_cursor is None and known==decision:return False
        if field_cursor is not None and ns(field_cursor)>ns(cursor):return False
    elif known==decision:return False
    return True

def validate_expression(expr):
    if not isinstance(expr,dict):raise ValueError('Expression must be an object')
    tags=set(expr)&{'const','field','op'}
    if len(tags)!=1:raise ValueError('Expression requires one discriminator')
    tag=next(iter(tags))
    allowed={'const':{'const'},'field':{'field','definition_id'},'op':{'op','args'}}[tag]
    if set(expr)-allowed:raise ValueError('Unexpected expression keys')
    if tag=='field':
        if not isinstance(expr['field'],str) or not expr['field']:raise ValueError('Invalid field name')
    elif tag=='op':
        op=expr['op'];args=expr.get('args')
        if op not in OPS or not isinstance(args,list) or not args or (op in ARITY and len(args)!=ARITY[op]):
            raise ValueError('Unsupported expression or arity')
        for arg in args:validate_expression(arg)
    return True

def evaluate(expr,context):
    validate_expression(expr)
    decision=ns(context['decision_ns'])
    if 'const' in expr:
        return expr['const'] if valid(expr['const']) else UNKNOWN
    if 'field' in expr:
        field=context.get('fields',{}).get(expr['field'])
        if not available(field,context) or field.get('status')!='observed' or not valid(field['value']):
            return UNKNOWN
        bound=context.get('definitions',{}).get(expr['field'])
        expected=expr.get('definition_id',bound)
        if not expected or expected!=field.get('definition_id'):return UNKNOWN
        if bound is not None and bound!=expected:return UNKNOWN
        return field['value']
    op=expr.get('op');args=expr.get('args',[])
    if op not in OPS or not args or (op in ARITY and len(args)!=ARITY[op]):
        raise ValueError('Unsupported expression or arity')
    values=[evaluate(arg,context) for arg in args]
    if op in {'and','or','not'}:
        if any(v is not UNKNOWN and type(v) is not bool for v in values):
            raise ValueError('Logical operands must be booleans')
        if op=='and' and False in values:return False
        if op=='or' and True in values:return True
        if any(v is UNKNOWN for v in values):return UNKNOWN
        return not values[0] if op=='not' else all(values) if op=='and' else any(values)
    if any(v is UNKNOWN for v in values):return UNKNOWN
    a=values[0];b=values[1] if len(values)>1 else None
    if op=='eq':return a==b
    if op=='ne':return a!=b
    if op=='in':return a in b
    if op in {'gt','ge','lt','le'}:
        return {'gt':lambda:a>b,'ge':lambda:a>=b,'lt':lambda:a<b,'le':lambda:a<=b}[op]()
    if any(isinstance(v,bool) or not isinstance(v,(float,int)) for v in values):
        raise ValueError('Arithmetic operands must be finite numbers')
    if op=='div' and b==0:return UNKNOWN
    result={'add':lambda:sum(values),'sub':lambda:a-b,'mul':lambda:reduce(mul,values,1),'div':lambda:a/b,'abs':lambda:abs(a),'sign':lambda:(a>0)-(a<0),'min':lambda:min(values),'max':lambda:max(values)}[op]()
    return result if valid(result) else UNKNOWN

def fields_in(expr):
    if isinstance(expr,dict):
        if 'field' in expr:yield expr['field']
        for value in expr.values():yield from fields_in(value)
    elif isinstance(expr,list):
        for value in expr:yield from fields_in(value)

def validate_rule(rule):
    for key in ['id','paper_included','entry','direction','exit','requires']:
        if key not in rule:raise ValueError('Missing rule field: '+key)
    if rule['paper_included'] is not True:raise ValueError('Every candidate must remain included')
    if not rule['id']:raise ValueError('Empty rule identifier')
    expressions=[rule['entry'].get('condition',rule['entry']),rule['direction']]
    if 'condition' in rule['exit']:expressions.append(rule['exit']['condition'])
    if rule.get('invalidation'):expressions.append(rule['invalidation'])
    for expr in expressions:validate_expression(expr)
    for expr in [expressions[0]]+([rule['invalidation']] if rule.get('invalidation') else []):
        if 'const' in expr and type(expr['const']) is not bool:raise ValueError('Condition must be boolean')
    if 'const' in rule['direction'] and (type(rule['direction']['const']) is not int or rule['direction']['const'] not in {-1,0,1}):
        raise ValueError('Direction must be -1, 0 or 1')
    used=set(fields_in([rule['entry'],rule['direction'],rule['exit'],rule.get('invalidation',{})]))
    for name in used:
        metadata=rule['requires'].get(name)
        if not metadata or not metadata.get('definition_id'):
            raise ValueError('Missing input definition: '+name)
        if metadata.get('role') not in {'feature','decision_state','execution_state'}:
            raise ValueError('Outcome/control metadata cannot be an entry feature: '+name)
    def check_binding(expr):
        if 'field' in expr and 'definition_id' in expr and expr['definition_id']!=rule['requires'][expr['field']]['definition_id']:
            raise ValueError('Expression conflicts with required definition')
        for arg in expr.get('args',[]):check_binding(arg)
    for expr in expressions:check_binding(expr)
    if not isinstance(rule['exit'],dict) or not ({'after_ns','condition'} & set(rule['exit'])):
        raise ValueError('Missing exit deadline or condition')
    if 'after_ns' in rule['exit'] and ns(rule['exit']['after_ns'])<=0:
        raise ValueError('Exit duration must be positive')
    return True

def evaluate_rule(rule,context):
    """Evaluate entry/direction only; this does not submit orders or simulate fills."""
    validate_rule(rule)
    bound=dict(context,definitions={k:v['definition_id'] for k,v in rule['requires'].items()})
    condition=evaluate(rule['entry'].get('condition',rule['entry']),bound)
    direction=evaluate(rule['direction'],bound)
    if condition is not UNKNOWN and type(condition) is not bool:raise ValueError('Condition must be boolean')
    if direction is not UNKNOWN and (type(direction) is not int or direction not in {-1,0,1}):
        raise ValueError('Direction must be -1, 0 or 1')
    return {'condition':condition,'direction':direction}
