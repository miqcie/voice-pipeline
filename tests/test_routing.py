"""Eval runner for voice pipeline routing accuracy.

Usage:
    uv run python -m pytest tests/test_routing.py -v
    uv run python -m pytest tests/test_routing.py -v -k "clear_signal"
"""

import json
from pathlib import Path

import pytest

from voice_pipeline.process import process_text

FIXTURES_DIR = Path(__file__).parent / "fixtures"
EXPECTED_DIR = Path(__file__).parent / "expected"


def load_expected_results() -> list[dict]:
    """Load all expected result JSON files."""
    results = []
    if not EXPECTED_DIR.exists():
        return results
    for f in sorted(EXPECTED_DIR.glob("*.json")):
        results.append(json.loads(f.read_text()))
    return results


def load_text_fixtures() -> dict[str, str]:
    """Load text fixtures as id -> text mapping."""
    texts = {}
    text_dir = FIXTURES_DIR / "text"
    if not text_dir.exists():
        return texts
    for f in sorted(text_dir.glob("*.txt")):
        fixture_id = f.stem
        texts[fixture_id] = f.read_text().strip()
    return texts


# Collect test cases from fixtures
_expected = load_expected_results()
_texts = load_text_fixtures()


@pytest.fixture
def text_fixtures():
    return _texts


@pytest.fixture
def expected_results():
    return _expected


# -- Parametric tests from fixtures --

def _get_text_test_cases() -> list[tuple[str, str, str]]:
    """Return (id, input_text, expected_destination) tuples."""
    cases = []
    for exp in _expected:
        fixture_id = exp["id"]
        # Use text from expected.input or from text fixture file
        text = exp.get("input") or _texts.get(fixture_id, "")
        if text:
            cases.append((fixture_id, text, exp["expected_destination"]))
    return cases


_test_cases = _get_text_test_cases()


@pytest.mark.skipif(not _test_cases, reason="No test fixtures found")
@pytest.mark.parametrize("fixture_id,input_text,expected_dest", _test_cases)
def test_destination_routing(fixture_id, input_text, expected_dest):
    """Test that voice notes route to the correct destination."""
    result = process_text(input_text)
    actual_dest = result.get("destination")
    assert actual_dest == expected_dest, (
        f"[{fixture_id}] Expected '{expected_dest}', got '{actual_dest}'\n"
        f"Input: {input_text[:100]}...\n"
        f"Full result: {json.dumps(result, indent=2)}"
    )


@pytest.mark.skipif(not _test_cases, reason="No test fixtures found")
@pytest.mark.parametrize("fixture_id,input_text,expected_dest", _test_cases)
def test_cleaned_text_not_empty(fixture_id, input_text, expected_dest):
    """Test that cleaned_text is always returned and non-empty."""
    result = process_text(input_text)
    cleaned = result.get("cleaned_text", "")
    assert cleaned and len(cleaned) > 0, (
        f"[{fixture_id}] cleaned_text is empty"
    )


@pytest.mark.skipif(not _test_cases, reason="No test fixtures found")
@pytest.mark.parametrize("fixture_id,input_text,expected_dest", _test_cases)
def test_valid_json_structure(fixture_id, input_text, expected_dest):
    """Test that result has all required fields."""
    result = process_text(input_text)
    assert "destination" in result, f"[{fixture_id}] Missing 'destination'"
    assert "cleaned_text" in result, f"[{fixture_id}] Missing 'cleaned_text'"
    assert "metadata" in result, f"[{fixture_id}] Missing 'metadata'"


# -- Summary reporter --

def test_routing_accuracy_summary():
    """Print overall routing accuracy (not a pass/fail test)."""
    if not _test_cases:
        pytest.skip("No test fixtures")

    correct = 0
    total = len(_test_cases)
    failures = []

    for fixture_id, input_text, expected_dest in _test_cases:
        try:
            result = process_text(input_text)
            if result.get("destination") == expected_dest:
                correct += 1
            else:
                failures.append(
                    f"  {fixture_id}: expected={expected_dest}, got={result.get('destination')}"
                )
        except Exception as e:
            failures.append(f"  {fixture_id}: ERROR - {e}")

    accuracy = correct / total * 100 if total else 0
    print(f"\n{'='*50}")
    print(f"Routing Accuracy: {correct}/{total} ({accuracy:.0f}%)")
    if failures:
        print(f"Failures:")
        for f in failures:
            print(f)
    print(f"{'='*50}\n")
