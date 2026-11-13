import unittest
from rebuild_fields import latest_ties, lifecycle_projection, book_projection


class ReconstructionTests(unittest.TestCase):
    def test_asof_retains_ties_and_excludes_future(self):
        rows=[{'known_by_ns':9,'id':'a'}, {'known_by_ns':10,'id':'b'},
              {'known_by_ns':10,'id':'c'}, {'known_by_ns':11,'id':'future'}]
        self.assertEqual([x['id'] for x in latest_ties(rows,10)],['b','c'])
        self.assertEqual(latest_ties(rows,8),[])

    def test_reset_is_not_replace_and_empty_is_observed_zero(self):
        events=[{'original_message':{'action':a},'original_effect':{}} for a in 'AMRCTF']
        self.assertEqual([x['original_message']['action'] for x in lifecycle_projection(events,'L033')],['M'])
        self.assertEqual([x['original_message']['action'] for x in lifecycle_projection(events,'L036')],['R'])
        self.assertEqual(lifecycle_projection([], 'L031'),[])

    def test_fifo_preserves_each_order_and_ahead(self):
        queue=[{'order_id':1,'size':3,'volume_ahead':0,'priority_age_s':2},
               {'order_id':2,'size':7,'volume_ahead':3,'priority_age_s':1}]
        b={'bid_levels_full':[{'price_raw':100,'size':10,'order_count':2,'fifo_queue':queue}],
           'ask_levels_full':[]}
        self.assertEqual(book_projection(b,'L041')['bid'][0]['fifo_queue'],queue)
        self.assertEqual(book_projection(b,'L044')['bid'][0]['orders'][1]['volume_ahead'],3)


if __name__=='__main__':
    unittest.main()
