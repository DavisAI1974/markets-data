import unittest
from remaining_fields import eligible_end, path_delta, state_hash


class RemainingFieldsTests(unittest.TestCase):
    def test_clock_tie_requires_eligible_cursor(self):
        ns = 1696247018981998588
        keys = [(ns - 1, 999), (ns, 3), (ns, 4), (ns + 1, 0)]
        self.assertEqual(eligible_end(keys, ns, 3), 2)
        self.assertEqual(eligible_end(keys, ns - 2, 1000), 0)

    def test_path_delta_retains_zero_missing_and_integer_clocks(self):
        a = {'receive_ns': 1696247018981998588, 'price_raw': 0,
             'bid_depth': 3, 'ask_depth': None, 'signed_trade_size': 4}
        b = dict(a, receive_ns=a['receive_ns'] + 1, price_raw=1000000,
                 bid_depth=0, signed_trade_size=-2)
        d = path_delta(a, b)
        self.assertEqual(d['elapsed_receive_ns'], 1)
        self.assertEqual(d['price_raw_change'], 1000000)
        self.assertEqual(d['bid_depth_change'], -3)
        self.assertIsNone(d['ask_depth_change'])
        self.assertIsNone(path_delta(None, b)['elapsed_receive_ns'])

    def test_hash_chain_detects_value_and_prior_change(self):
        a = {'clock_ns': 1696247018981998588, 'value': None}
        self.assertNotEqual(state_hash(a, '0'*64), state_hash(dict(a, value=0), '0'*64))
        self.assertNotEqual(state_hash(a, '0'*64), state_hash(a, '1'*64))


if __name__ == '__main__':
    unittest.main()
