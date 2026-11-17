"""Bonus: DeepEval port agrees with the pydantic-evals graders. Skipped when deepeval is not installed."""
import pytest

pytestmark = pytest.mark.student
pytest.importorskip("deepeval")


@pytest.mark.parametrize("shape,spec", [("fixed", "config/metric_spec.yaml"), ("seeded_regression", "config/metric_spec.yaml")])
def test_deepeval_matches_pydantic_evals(shape, spec):
    from pathlib import Path
    from lab9.deepeval_port import compare
    from lab9.eval import load_spec

    n, diffs = compare(shape, load_spec(Path(spec)))
    assert n > 0 and diffs == []
