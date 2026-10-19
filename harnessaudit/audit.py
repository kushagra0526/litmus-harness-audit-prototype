"""Audit one hidden test suite against its task's reference solution.

audit(task_dir, suite_file) -> {
  broken:        tests that fail on the reference itself,
  gaps:          surviving mutants that really behave differently (witness input + both outputs), grouped by line,
  equivalent:    surviving mutants with no difference on random inputs (not reported as gaps),
  over_specified:{test: [reasons]} tests that fail on a semantics-preserving rewrite,
  kill_rate, coverage (baseline): uncovered reference lines }
"""
import ast
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from .mutate import mutants
from .rewrite import rewrites

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run(job, timeout=10):
    try:
        p = subprocess.run([sys.executable, "-m", "harnessaudit.runner"], input=json.dumps(job), capture_output=True,
                           text=True, timeout=timeout, cwd=ROOT)
        return json.loads(p.stdout) if p.stdout else {"failed": ["<crash>"], "stderr": p.stderr[-300:]}
    except subprocess.TimeoutExpired:
        return {"failed": ["<timeout>"]}  # a hanging submission fails the harness's time limit too


def gap_tags(src):
    return {i + 1: m.group(1) for i, line in enumerate(src.splitlines()) for m in [re.search(r"#\s*gap:(\w+)", line)] if m}


def audit(task_dir, suite_file, n=300, workers=8):
    ref = open(os.path.join(task_dir, "solution.py"), encoding="utf-8").read()
    suite = os.path.abspath(os.path.join(task_dir, suite_file))
    spec_path = os.path.abspath(os.path.join(task_dir, "spec.py"))
    spec_src = open(spec_path, encoding="utf-8").read()
    unordered = re.findall(r"['\"](\w+)['\"]", (re.search(r"UNORDERED\s*=\s*\[(.*?)\]", spec_src) or re.match("", "")).group(1) or "")
    base = {"suite": suite, "spec": spec_path, "ref": ref, "n": n}
    broken = _run({**base, "source": ref})["failed"]
    muts = list(mutants(ref))
    with ThreadPoolExecutor(workers) as ex:
        results = list(ex.map(lambda m: _run({**base, "source": m["source"], "diff": True}), muts))
    gaps, equivalent, killed = {}, [], 0
    for m, r in zip(muts, results):
        if r["failed"]:
            killed += 1
        elif r.get("diff"):
            gaps.setdefault(m["line"], []).append({"op": m["op"], **r["diff"]})
        else:
            equivalent.append({"line": m["line"], "op": m["op"]})
    over = {}
    rw = rewrites(ref, unordered)
    with ThreadPoolExecutor(workers) as ex:
        rres = dict(zip(rw, ex.map(lambda k: _run({**base, "source": rw[k][1], "diff": False}), rw)))
        sanity = dict(zip(rw, ex.map(lambda k: _run({**base, "suite": os.path.join(ROOT, "harnessaudit", "empty_suite.py"),
                                                     "source": rw[k][1], "diff": True}), rw)))
    for k, r in rres.items():
        if sanity[k].get("diff"):  # the rewrite changed behaviour: don't trust it
            continue
        for t in r["failed"]:
            if t not in broken and not t.startswith("<"):
                over.setdefault(t, []).append(rw[k][0])
    cov = _run({**base, "source": ref, "coverage": True}).get("lines", [])
    code_lines = {n.lineno for n in ast.walk(ast.parse(ref)) if isinstance(n, ast.stmt)
                  and not isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))
                  and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))}
    real = len(muts) - len(equivalent)
    return {"mutants": len(muts), "killed": killed, "equivalent": equivalent, "gaps": gaps,
            "kill_rate": round(killed / real, 3) if real else 1.0, "broken": broken, "over_specified": over,
            "uncovered_lines": sorted(code_lines - set(cov)), "line_coverage": round(len(code_lines & set(cov)) / len(code_lines), 3),
            "tags": gap_tags(ref), "reference_lines": ref.splitlines()}
