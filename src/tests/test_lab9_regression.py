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
