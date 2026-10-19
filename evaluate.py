"""Score the harness audit vs line coverage on tasks with planted harness defects.

python evaluate.py dev | heldout     (heldout tasks frozen in git before the first run)
"""
import json
import os
import sys

from harnessaudit.audit import audit


def score(split):
    root = os.path.join("tasks", split)
    tot = {"planted_gaps": 0, "gaps_found": 0, "coverage_found": 0, "unplanted_gap_reports": 0,
           "over_specified": 0, "over_found": 0, "false_over": 0, "fine_tests": 0, "equivalent_survivors": 0,
           "raw_survivors": 0, "full_suite_gap_reports": 0, "full_suite_false_over": 0, "broken": 0}
    rows = []
    for task in sorted(os.listdir(root)):
        labels = json.load(open(os.path.join(root, task, "labels.json")))
        for suite, lab in labels.items():
            r = audit(os.path.join(root, task), suite)
            tags = r["tags"]
            found = {tags[ln] for ln in r["gaps"] if ln in tags}
            unplanted = [ln for ln in r["gaps"] if ln not in tags]
            cov_found = {g for ln, g in tags.items() if ln in r["uncovered_lines"]}
            flagged = set(r["over_specified"])
            src = open(os.path.join(root, task, suite)).read()
            tests = {ln.split("(")[0][4:] for ln in src.splitlines() if ln.startswith("def test_")}
            planted = set(lab["gaps"])
            tot["planted_gaps"] += len(planted)
            tot["gaps_found"] += len(planted & found)
            tot["coverage_found"] += len(planted & cov_found)
            tot["over_specified"] += len(lab["over_specified"])
            tot["over_found"] += len(flagged & set(lab["over_specified"]))
            tot["false_over"] += len(flagged - set(lab["over_specified"]))
            tot["fine_tests"] += len(tests - set(lab["over_specified"]))
            tot["equivalent_survivors"] += len(r["equivalent"])
            tot["raw_survivors"] += len(r["equivalent"]) + sum(len(v) for v in r["gaps"].values())
            tot["broken"] += len(r["broken"])
            if suite == "tests_full.py":
                tot["full_suite_gap_reports"] += len(r["gaps"])
                tot["full_suite_false_over"] += len(flagged)
            else:
                tot["unplanted_gap_reports"] += len(unplanted)
            rows.append({"task": task, "suite": suite, "mutants": r["mutants"], "kill_rate": r["kill_rate"],
                         "line_coverage": r["line_coverage"], "planted": sorted(planted), "found": sorted(found),
                         "coverage_found": sorted(planted & cov_found), "unplanted_gap_lines": unplanted,
                         "over_specified_flagged": r["over_specified"], "equivalent": r["equivalent"],
                         "witnesses": {str(ln): v[0] for ln, v in r["gaps"].items()}})
    return tot, rows


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "dev"
    tot, rows = score(split)
    print(json.dumps(tot, indent=1))
    for r in rows:
        print(f"{r['task']:16} {r['suite']:14} mutants {r['mutants']:3} kill {r['kill_rate']:.2f} cov {r['line_coverage']:.2f} "
              f"gaps {r['found']}/{r['planted']} cov-found {r['coverage_found']} unplanted {r['unplanted_gap_lines']} "
              f"over {sorted(r['over_specified_flagged'])} equiv {len(r['equivalent'])}")
    os.makedirs("out", exist_ok=True)
    json.dump({"totals": tot, "rows": rows}, open(f"out/{split}.json", "w"), indent=1)
