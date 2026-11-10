import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from paper_rules.contract import UNKNOWN
from paper_rules.recovered import build_model_context, predict_bound_model, verify_recovery
from paper_rules import source_events

ROOT = Path(__file__).resolve().parents[1]
NS = 1_000_000_000


class RecoveredRuntimeTests(unittest.TestCase):
    def inputs(self):
        groups = [dict(receive_ns=i*NS, cursor=i, group_index=i, segment=0, valid=True,
                       bid_raw=100_000_000+i*1_000_000, ask_raw=102_000_000+i*1_000_000,
                       bid_lots=3, ask_lots=1, bid_orders=2, ask_orders=1)
                  for i in range(23)]
        flow = [dict(second=i, buy=1, sell=0, complete=True,
                     classification='previous_completed_group_midpoint', segment=0,
                     known_by_ns=(i+1)*NS, known_by_cursor=i+1) for i in range(2,22)]
        return groups, flow

    def test_source_feature_arithmetic(self):
        groups, flow = self.inputs()
        c = build_model_context(groups, flow,last_closed_second=21)
        f = c['fields']
        self.assertEqual(f['prior_ticks20']['value'],20)
        self.assertEqual(f['range_ticks20']['value'],20)
        self.assertEqual(f['touch_imb']['value'],0.5)
        self.assertEqual(f['early_buy']['value'],10)
        self.assertEqual(f['fresh_buy5']['value'],5)
        self.assertEqual(f['mi_flow']['value'],0)
        self.assertEqual(f['spread_ticks']['definition_id'],'source-M0M1-spread_ticks')

    def test_missing_bin_is_not_zero_flow(self):
        g,f=self.inputs()
        self.assertIs(build_model_context(g,f[:-1],last_closed_second=21),UNKNOWN)

    def test_native_flow_cannot_substitute_midpoint_flow(self):
        g,f=self.inputs();f[0]['classification']='native_aggressor'
        self.assertIs(build_model_context(g,f,last_closed_second=21),UNKNOWN)

    def test_reset_or_future_cursor_blocks_context(self):
        for field,value in [('segment',1),('known_by_cursor',99),('known_by_ns',24*NS)]:
            g,f=self.inputs();f[0][field]=value
            self.assertIs(build_model_context(g,f,last_closed_second=21),UNKNOWN)

    def test_invalid_intermediate_quote_blocks_context(self):
        g,f=self.inputs();g[12]['valid']=False
        self.assertIs(build_model_context(g,f,last_closed_second=21),UNKNOWN)

    def test_missing_group_cannot_masquerade_as_continuous_history(self):
        g,f=self.inputs();del g[10]
        self.assertIs(build_model_context(g,f,last_closed_second=21),UNKNOWN)

    def test_non_integer_price_cannot_enter_exact_price_features(self):
        g,f=self.inputs();g[10]['bid_raw']=110_000_000.5
        self.assertIs(build_model_context(g,f,last_closed_second=21),UNKNOWN)

    def test_recognition_window_cannot_be_silently_advanced(self):
        g,f=self.inputs()
        self.assertIs(build_model_context(g,f,last_closed_second=20),UNKNOWN)

    def test_history_coordinates_require_three_ordered_adjacent_prior_groups(self):
        self.assertFalse(source_events.history_coordinates([3,13,100,1000],[]))
        self.assertFalse(source_events.history_coordinates([3,13,100,1000],[[0,10,97,990],[2,12,98,1000],[1,11,99,1000]]))

    def test_missing_endpoint_is_unavailable(self):
        self.assertIsNone(source_events.endpoint([],100))

    def test_changed_source_binding_is_rejected(self):
        original=Path.read_bytes
        def changed(path):
            content=original(path)
            if path.name=='M0M1_BINDING_RECOVERY.json':return content.replace(b'prior_ticks20',b'prior_ticks99')
            return content
        with patch.object(Path,'read_bytes',changed):
            with self.assertRaises(ValueError):verify_recovery(ROOT)

    def test_empty_observed_flow_is_explicit_undefined(self):
        g,f=self.inputs()
        for row in f:row['buy']=row['sell']=0
        c=build_model_context(g,f,last_closed_second=21)
        self.assertEqual(c['fields']['mi_flow']['status'],'observed_undefined')
        self.assertIsNone(c['fields']['mi_flow']['value'])
        self.assertEqual(c['fields']['early_buy']['value'],0)

    def test_replay_uses_session_availability_without_backdating_market_clock(self):
        c=build_model_context(*self.inputs(),last_closed_second=21)
        recovery=verify_recovery(ROOT)
        result=predict_bound_model(recovery,'M0',c,artifact_available_session_ns=100,
                                   decision_session_ns=101,session_id='synthetic-acceptance')
        self.assertIsInstance(result,float)
        self.assertEqual(c['decision_ns'],22*NS)
        self.assertIs(predict_bound_model(recovery,'M0',c,artifact_available_session_ns=101,
                                         decision_session_ns=101,session_id='synthetic-acceptance'),UNKNOWN)

    def test_recovery_binds_original_state_and_definitions(self):
        r=verify_recovery(ROOT)
        self.assertEqual(len(r['features']),17)
        source=json.loads((ROOT/'machine/INITIAL_RULES_V2.json').read_text())
        self.assertEqual(r['models']['M1']['state'],source['models']['M1'])

    def test_all_independent_source_boundaries(self):
        cases=json.loads((ROOT/'recovery/ol_ex_independent_boundary_fixtures.json').read_text())['fixtures']
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertEqual(getattr(source_events,case['operation'])(*case['inputs']),case['expected'])


if __name__=='__main__':unittest.main()
