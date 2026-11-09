import unittest
from paper_rules.contract import UNKNOWN
from paper_rules.models import predict_frozen_linear

MODEL={'features':['x'],'imputation':[2.0],'center':[0.0,0.0],'scale':[1.0,1.0],'coefficients':[3.0,5.0],'intercept':7.0}
BINDINGS={'x':'original-feature/v1'}

class FrozenPredictionTests(unittest.TestCase):
    def context(self,value,status='observed',known='99'):
        return {'decision_ns':'100','fields':{'x':{'value':value,'status':status,'role':'feature','known_by_ns':known,'definition_id':'original-feature/v1'}}}

    def test_matches_manual_linear_calculation(self):
        self.assertEqual(predict_frozen_linear(MODEL,self.context(4),BINDINGS,'90'),19)

    def test_observed_undefined_uses_frozen_imputation_and_missing_flag(self):
        self.assertEqual(predict_frozen_linear(MODEL,self.context(None,'observed_undefined'),BINDINGS,'90'),18)

    def test_feed_failure_cannot_become_training_mean(self):
        self.assertIs(predict_frozen_linear(MODEL,self.context(None,'feed_missing'),BINDINGS,'90'),UNKNOWN)

    def test_future_feature_cannot_be_imputed_as_missing(self):
        self.assertIs(predict_frozen_linear(MODEL,self.context(4,known='101'),BINDINGS,'90'),UNKNOWN)

    def test_unfrozen_or_future_model_cannot_predict(self):
        self.assertIs(predict_frozen_linear(MODEL,self.context(4),BINDINGS,'101'),UNKNOWN)

    def test_feature_definition_mismatch_is_unavailable(self):
        self.assertIs(predict_frozen_linear(MODEL,self.context(4),{'x':'different-native-source'},'90'),UNKNOWN)

    def test_bad_dimensions_are_rejected(self):
        with self.assertRaises(ValueError):predict_frozen_linear(dict(MODEL,coefficients=[1]),self.context(4),BINDINGS,'90')

if __name__=='__main__':unittest.main()
