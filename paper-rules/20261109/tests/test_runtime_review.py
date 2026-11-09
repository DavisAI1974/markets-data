"""Independent synthetic regressions from review_runtime.json; no market replay."""
import unittest

from paper_rules import contract
from paper_rules.models import predict_frozen_linear


MODEL = {
    'features': ['x'], 'imputation': [2.0], 'center': [0.0, 0.0],
    'scale': [1.0, 1.0], 'coefficients': [3.0, 5.0], 'intercept': 7.0,
}
BINDINGS = {'x': 'expected/v1'}


def context(**overrides):
    field = {'value': 4, 'known_by_ns': '100', 'known_by_cursor': 10,
             'definition_id': 'expected/v1', 'status': 'observed', 'role': 'feature'}
    field.update(overrides)
    return {'decision_ns': '100', 'decision_cursor': 10, 'fields': {'x': field}}


def rule():
    return {
        'id': 'synthetic', 'paper_included': True,
        'entry': {'condition': {'op': 'gt', 'args': [{'field': 'x'}, {'const': 0}]}},
        'direction': {'const': 1}, 'exit': {'after_ns': '20'},
        'requires': {'x': {'definition_id': 'expected/v1', 'role': 'feature'}},
    }


class RuntimeReviewRegressions(unittest.TestCase):
    def test_expression_rejects_unavailable_status_even_with_numeric_value(self):
        for status in ('feed_missing', 'unknown_availability', 'future_known_by',
                       'definition_mismatch'):
            with self.subTest(status=status):
                self.assertIs(contract.evaluate(
                    {'field': 'x', 'definition_id': 'expected/v1'},
                    context(status=status)), contract.UNKNOWN)

    def test_model_requires_explicit_null_for_observed_undefined(self):
        ctx = context(status='observed_undefined')
        del ctx['fields']['x']['value']
        try:
            result = predict_frozen_linear(MODEL, ctx, BINDINGS, '90')
        except ValueError:
            return  # A schema rejection is also fail-closed.
        self.assertIs(result, contract.UNKNOWN)

    def test_model_rejects_outcome_role(self):
        self.assertIs(predict_frozen_linear(
            MODEL, context(role='outcome'), BINDINGS, '90'), contract.UNKNOWN)

    def test_expression_rejects_later_cursor_at_same_nanosecond(self):
        self.assertIs(contract.evaluate(
            {'field': 'x', 'definition_id': 'expected/v1'},
            context(known_by_cursor=11)), contract.UNKNOWN)

    def test_model_rejects_later_cursor_at_same_nanosecond(self):
        self.assertIs(predict_frozen_linear(
            MODEL, context(known_by_cursor=11), BINDINGS, '90'), contract.UNKNOWN)

    def test_equal_cursor_is_available(self):
        self.assertEqual(contract.evaluate(
            {'field': 'x', 'definition_id': 'expected/v1'}, context()), 4)
        self.assertEqual(predict_frozen_linear(MODEL, context(), BINDINGS, '90'), 19)

    def test_unknown_operator_fails_validation(self):
        candidate = rule()
        candidate['entry']['condition'] = {'op': 'nonsense', 'args': []}
        with self.assertRaises(ValueError):
            contract.validate_rule(candidate)

    def test_non_direction_constant_fails_validation(self):
        candidate = rule()
        candidate['direction'] = {'const': 'LONG'}
        with self.assertRaises(ValueError):
            contract.validate_rule(candidate)

    def test_conflicting_expression_and_required_definition_fails_validation(self):
        candidate = rule()
        candidate['entry']['condition']['args'][0]['definition_id'] = 'wrong/v1'
        with self.assertRaises(ValueError):
            contract.validate_rule(candidate)

    def test_evaluate_rule_binds_required_definition_without_expression_repetition(self):
        ctx = context()
        ctx['definitions'] = {'x': 'caller-override/v1'}
        self.assertEqual(contract.evaluate_rule(rule(), ctx),
                         {'condition': True, 'direction': 1})
        self.assertEqual(ctx['definitions'], {'x': 'caller-override/v1'})

    def test_evaluate_rule_rejects_wrong_bound_feature(self):
        result = contract.evaluate_rule(rule(), context(definition_id='wrong/v1'))
        self.assertIs(result['condition'], contract.UNKNOWN)
        self.assertEqual(result['direction'], 1)

    def test_evaluate_rule_defaults_missing_status_or_role_to_unknown(self):
        for key in ('status', 'role'):
            with self.subTest(key=key):
                ctx = context()
                del ctx['fields']['x'][key]
                self.assertIs(contract.evaluate_rule(rule(), ctx)['condition'],
                              contract.UNKNOWN)

    def test_standalone_field_without_definition_is_unknown(self):
        self.assertIs(contract.evaluate({'field': 'x'}, context()), contract.UNKNOWN)

    def test_malformed_expression_rejected(self):
        cases = [
            {'const': 1, 'field': 'x'},
            {'field': 'x', 'typo': True},
            {'op': 'gt', 'args': [{'const': 1}]},
            {'op': 'and'},
            {'op': 'add', 'args': []},
        ]
        for expression in cases:
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    contract.evaluate(expression, context())

    def test_model_binding_cannot_be_empty_or_null(self):
        for definition in (None, ''):
            with self.subTest(definition=definition):
                ctx = context(definition_id=definition)
                if definition is None:
                    del ctx['fields']['x']['definition_id']
                try:
                    result = predict_frozen_linear(MODEL, ctx, {'x': definition}, '90')
                except ValueError:
                    continue
                self.assertIs(result, contract.UNKNOWN)

    def test_exit_constant_condition_requires_boolean(self):
        candidate = rule()
        candidate['exit'] = {'condition': {'const': 1}}
        with self.assertRaises(ValueError):
            contract.validate_rule(candidate)


if __name__ == '__main__':
    unittest.main()
