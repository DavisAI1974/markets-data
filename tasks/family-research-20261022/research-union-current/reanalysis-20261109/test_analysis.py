import unittest
import numpy as np
from analyze import delayed_return, relation, sign, ridge, window_availability

class AnalysisTests(unittest.TestCase):
    def test_confirmation_move_is_not_earned_after_entry(self):
        self.assertEqual(delayed_return(3,2,1),1)
        self.assertEqual(delayed_return(-3,-2,-1),1)
        self.assertEqual(delayed_return(0,2,1),-2)

    def test_unknown_completion_is_unavailable(self):
        self.assertEqual(window_availability([(1,0,0,None)],100),(False,'unknown_completion',None))

    def test_future_completion_is_not_admitted(self):
        self.assertEqual(window_availability([(1,0,0,101)],100),(False,'not_yet_known',101))
        self.assertEqual(window_availability([(1,0,0,100)],100),(True,'available',100))

    def test_missing_and_balanced_are_different(self):
        self.assertEqual(relation(sign(np.nan),sign(1)),'missing')
        self.assertEqual(relation(sign(0),sign(1)),'neutral')

    def test_test_population_does_not_change_fitted_prediction(self):
        train=np.array([[1.,0],[2.,np.nan],[3.,1],[4.,2]])
        target=np.array([0.,1.,2.,3.])
        a=ridge(train,target,np.array([[2.,np.nan]]))[0]
        b=ridge(train,target,np.array([[2.,np.nan],[10000.,10000.]]))[0]
        self.assertAlmostEqual(a,b)

if __name__=='__main__':unittest.main(verbosity=2)
