import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from harnessaudit.audit import audit  # noqa: E402
from harnessaudit.mutate import mutants  # noqa: E402
from harnessaudit.rewrite import rewrites  # noqa: E402
from harnessaudit.runner import shrink  # noqa: E402

SRC = "def f(x, _y=1):\n    if x <= 0:\n        raise ValueError('neg')\n    return [x, _y]\n"


def test_mutants_include_boundary_flip_and_deletion():
    ops = {(m["line"], m["op"]) for m in mutants(SRC)}
    assert (2, "LtE -> Lt") in ops and (3, "delete statement") in ops and (4, "return None") in ops


def test_rewrites_keep_behaviour_but_change_surface():
    rw = rewrites(SRC, unordered=["f"])
    assert "_r_y" in rw["rename_private"][1]
    assert "invalid input (NEG)" in rw["reword_errors"][1]
    assert "reversed" in rw["reorder_unordered"][1]


def test_shrink_keeps_only_what_triggers_the_difference():
    assert shrink((3, [1, 9, 2, 9]), lambda c: 9 in c[1]) == (3, [9])


def test_full_coverage_suite_still_has_gaps_with_witnesses():
    r = audit("tasks/dev/lru_cache", "tests_weak.py")
    assert r["line_coverage"] == 1.0
    assert {r["tags"][ln] for ln in r["gaps"]} == {"cap_zero", "get_refresh"}
    assert r["gaps"][7][0]["case"] == "(0, [])"


def test_equivalent_mutants_are_not_reported():
    r = audit("tasks/dev/rate_limiter", "tests_full.py")
    assert r["gaps"] == {} and len(r["equivalent"]) == 3  # e.g. not storing the filtered list on reject


def test_over_specified_tests_named_and_complete_suite_clean():
    weak = audit("tasks/dev/paginate", "tests_weak.py")
    full = audit("tasks/dev/paginate", "tests_full.py")
    assert set(weak["over_specified"]) == {"test_page_zero_message"} and full["over_specified"] == {}
