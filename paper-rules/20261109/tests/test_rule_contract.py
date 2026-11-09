import unittest
from paper_rules.contract import evaluate, validate_rule, UNKNOWN


class CausalExpressionTests(unittest.TestCase):
    def context(self, value=3, known='1696235372000000001'):
        return {'decision_ns':'1696235372000000001','decision_cursor':10,'definitions':{'flow':'native-flow5/v1'},'fields':{'flow':{'value':value,'known_by_ns':known,'known_by_cursor':10,'status':'observed','role':'feature','definition_id':'native-flow5/v1'}}}

    def test_one_nanosecond_future_input_is_unavailable(self):
        self.assertIs(evaluate({'field':'flow'},self.context(known='1696235372000000002')),UNKNOWN)

    def test_exact_decision_boundary_is_available(self):
        self.assertEqual(evaluate({'field':'flow'},self.context()),3)

    def test_missing_is_not_false_under_negation(self):
        self.assertIs(evaluate({'op':'not','args':[{'field':'absent'}]},self.context()),UNKNOWN)

    def test_undefined_ratio_does_not_become_zero(self):
        self.assertIs(evaluate({'op':'div','args':[{'const':0},{'const':0}]},self.context()),UNKNOWN)

    def test_defined_zero_is_preserved(self):
        self.assertEqual(evaluate({'op':'sign','args':[{'field':'flow'}]},self.context(0)),0)

    def test_nonfinite_value_is_unavailable(self):
        self.assertIs(evaluate({'field':'flow'},self.context(float('nan'))),UNKNOWN)

    def test_float_nanosecond_clock_is_rejected(self):
        c=self.context();c['decision_ns']=1696235372000000001.0
        with self.assertRaises(ValueError):evaluate({'field':'flow'},c)

    def test_wrong_feature_definition_is_unavailable(self):
        self.assertIs(evaluate({'field':'flow','definition_id':'midpoint-proxy-flow5/v1'},self.context()),UNKNOWN)

    def test_future_label_cannot_be_a_feature(self):
        r={'id':'test','paper_included':True,'entry':{'condition':{'field':'future_price20'}},'direction':{'const':1},'exit':{'after_ns':'20000000000'},'requires':{'future_price20':{'role':'outcome','definition_id':'x'}}}
        with self.assertRaises(ValueError):validate_rule(r)

    def test_cannot_exclude_a_candidate_by_paper_flag(self):
        r={'id':'test','paper_included':False,'entry':{'condition':{'const':True}},'direction':{'const':1},'exit':{'after_ns':'20000000000'},'requires':{}}
        with self.assertRaises(ValueError):validate_rule(r)

    def test_missing_definition_cannot_pass_rule_validation(self):
        r={'id':'test','paper_included':True,'entry':{'condition':{'field':'flow'}},'direction':{'const':1},'exit':{'after_ns':'20000000000'},'requires':{}}
        with self.assertRaises(ValueError):validate_rule(r)


if __name__=='__main__':unittest.main()
