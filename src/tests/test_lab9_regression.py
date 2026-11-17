"""M3 regression: FM-08 (reply != ledger) is invisible to the ledger-only metric."""
import pytest

pytestmark = pytest.mark.student


def test_misreport_caught_only_by_reply_matches_ledger():
    from lab8.shapes import SHAPES
    from lab9 import eval as E
    from lab9.variant_agent import make_shape
    from lab9.variants import register

    register()
    SHAPES["t_misreport"] = make_shape("t_misreport", frozenset({"no_override", "misreport"}))
    rep = E.run_eval("t_misreport", E.load_spec(), seeds=[11])["metrics"]
    assert rep["refund_amount_correct"] == 1.0
    assert rep["reply_matches_ledger"] < 0.95


def test_fixed_has_no_false_alarm():
    from lab9 import eval as E
    from lab9.variants import register

    register()
    assert E.run_eval("fixed", E.load_spec(), seeds=[11])["metrics"]["reply_matches_ledger"] == 1.0


def _rep(rows, **kw):
    return {"manifest": {"eval_set_sha": "x", "items": 2, "seeds": [1, 2]}, "rows": rows,
            "metrics": {"pass_rate": 1.0}, "evaluator_failures": [], **kw}


_ROWS = [{"item_id": f"E-{i}", "seed": s, "pass_rate": True, "slices": ["money_movement"]}
         for i in (1, 2) for s in (1, 2)]
_SPEC = {"eval_set_version": "v2", "metrics": [{"id": "pass_rate", "kind": "capability"}], "slices": []}


def test_integrity_duplicate_rows_and_evaluator_failures():
    import copy
    from lab9 import gate

    base = _rep(copy.deepcopy(_ROWS))
    dup = copy.deepcopy(_ROWS)
    dup[0] = copy.deepcopy(dup[1])
    assert gate.integrity_check(_rep(dup), base, _SPEC)
    assert gate.integrity_check(_rep(copy.deepcopy(_ROWS), evaluator_failures=[{"e": 1}]), base, _SPEC)


def test_integrity_slice_relabel_and_ratchet():
    import copy
    from lab9 import gate

    base = _rep(copy.deepcopy(_ROWS))
    rel = copy.deepcopy(_ROWS)
    rel[0]["slices"] = []
    assert gate.integrity_check(_rep(rel), base, _SPEC)
    old = dict(_SPEC, slices=[{"name": "money_movement", "metric": "pass_rate", "min": 0.9, "blocking": True}])
    assert gate.integrity_check(base, base, _SPEC, old)            # slice dropped
    assert gate.integrity_check(base, base, old, old) == []
