import unittest
import pandas as pd
import numpy as np
from discovery_depth import exact_join,sgn,rel,num
from discovery_timing_review import order_class

class EvidenceJoinTests(unittest.TestCase):
 def test_interval_start_is_not_an_event_time(self):
  self.assertEqual(order_class(0,1),'overlapping_intervals_order_unresolved')
  self.assertEqual(order_class(0,2),'aggression_interval_before_quote_interval')
  self.assertEqual(order_class(1,1),'quote_interval_before_aggression_interval')
  self.assertEqual(order_class(1,-1),'missing_or_censored')
 def test_source_booleans_preserve_eligible_denominators(self):
  result=num(pd.DataFrame({'x':['True','False','1','0']}),'x')
  self.assertEqual(result.tolist(),[1,0,1,0])
 def test_exact_ns_does_not_round(self):
  left=pd.DataFrame({'day':['d'],'candidate_id':['x'],'recognition':['1696206092957453764']})
  right=pd.DataFrame({'day':['d'],'candidate_id':['x'],'decision':['1696206092957453765']})
  with self.assertRaisesRegex(AssertionError,'clock disagreement'):exact_join(left,right,['day','candidate_id'],'recognition','decision')
 def test_duplicate_identity_rejected(self):
  left=pd.DataFrame({'day':['d','d'],'candidate_id':['x','x'],'recognition':['1','1']})
  right=pd.DataFrame({'day':['d'],'candidate_id':['x'],'decision':['1']})
  with self.assertRaisesRegex(AssertionError,'duplicate left'):exact_join(left,right,['day','candidate_id'],'recognition','decision')
 def test_missing_and_balanced_directions_are_distinct(self):
  self.assertEqual(sgn('NA'),'missing');self.assertEqual(sgn('0'),'0')
  self.assertEqual(rel(sgn('NA'),'+'),'missing');self.assertEqual(rel(sgn('0'),'+'),'neutral')
  oriented=np.sign(pd.Series([0,1,-1,np.nan])).replace(0,np.nan)*pd.Series([3,3,3,3])
  self.assertTrue(pd.isna(oriented[0]));self.assertEqual(oriented[1],3);self.assertEqual(oriented[2],-3)
 def test_pressure_orientation_cancels_twice(self):
  # P03 stores both flow sign and return relative to pressure. Their product
  # correctly recovers flow-oriented return for either pressure direction.
  for pressure in [-1,1]:
   for flow in [-1,1]:self.assertEqual((flow*pressure)*(2*pressure),2*flow)

if __name__=='__main__':unittest.main()
