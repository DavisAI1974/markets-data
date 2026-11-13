import unittest
from audit import measured_leaves, clock_int, available


class AvailabilityTests(unittest.TestCase):
    def test_missing_placeholder_is_not_measured_zero(self):
        record = {'state': 'MISSING', 'state_code': 1, 'raw_float64': 0.0}
        self.assertEqual(list(measured_leaves(record)), [])

    def test_present_zero_remains_measurement(self):
        record = {'state': 'PRESENT', 'state_code': 0, 'raw_float64': 0.0}
        self.assertEqual(list(measured_leaves(record)), [('raw_float64', 0.0)])

    def test_invalid_state_disagreement_is_not_measured(self):
        record = {'state': 'MISSING', 'state_code': 0, 'raw_float64': 3.0}
        self.assertEqual(list(measured_leaves(record)), [])

    def test_ids_clocks_and_state_codes_are_not_measurements(self):
        self.assertEqual(list(measured_leaves({'known_by_ns': 1697660175489954980,
            'order_id': 23, 'group_ordinal': 8, 'size': 1, 'state': 0})), [('size', 1)])

    def test_nanoseconds_do_not_round(self):
        self.assertEqual(clock_int('1697660175489954981'), 1697660175489954981)
        self.assertFalse(available('1697660175489954981', '1697660175489954980'))
        self.assertTrue(available('1697660175489954980', '1697660175489954980'))

    def test_missing_clock_is_unknown_not_available(self):
        self.assertIsNone(available(None, 100))
        self.assertIsNone(available('', 100))

    def test_external_missing_state_does_not_admit_value(self):
        self.assertEqual(list(measured_leaves({'published_ns': 5, 'state': 1, 'value': 0})), [])

    def test_nested_original_numeric_payload_remains_separate(self):
        self.assertEqual(list(measured_leaves({'before': {'effect_json': '{"added":2,"removed":3}'}})),
                         [('before.effect_json.added', 2), ('before.effect_json.removed', 3)])


if __name__ == '__main__':
    unittest.main()
