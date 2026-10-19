"""Subprocess worker: load a candidate source as module `solution`, run the hidden suite, optionally
differential-check it against the reference on random inputs, or record line coverage.
stdin: JSON job, stdout: JSON result. Run as: python -m harnessaudit.runner"""
import copy
import importlib.util
import json
import random
import sys
import types


def load_source(src, name="solution"):
    m = types.ModuleType(name)
    m.__file__ = f"<{name}>"
    exec(compile(src, f"<{name}>", "exec"), m.__dict__)
    return m


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run_suite(mod, suite):
    failed = []
    for name in sorted(n for n in dir(suite) if n.startswith("test_")):
        try:
            getattr(suite, name)(mod)
        except Exception:  # an assertion or any crash = the test fails
            failed.append(name)
    return failed


def observe(spec, mod, case):
    try:
        return ("ok", spec.observe(mod, copy.deepcopy(case)))
    except Exception as e:  # spec-aware equivalence: exceptions compare by type only
        return ("raise", type(e).__name__)


def differential(spec, ref, mod, n, seed):
    rng, best = random.Random(seed), None
    differs = lambda c: observe(spec, ref, c) != observe(spec, mod, c)
    for _ in range(n):
        case = spec.gen(rng)
        if differs(case) and (best is None or len(repr(case)) < len(repr(best))):  # keep the smallest witness
            best = case
    if best is None:
        return None
    best = shrink(best, differs)
    a, b = observe(spec, ref, best), observe(spec, mod, best)
    return {"case": repr(best), "reference": repr(a[1] if a[0] == "ok" else "raises " + a[1]),
            "candidate": repr(b[1] if b[0] == "ok" else "raises " + b[1])}


def shrink(case, differs):
    """Greedily drop list elements (e.g. operations) while the difference remains."""
    if isinstance(case, list):
        i = 0
        while i < len(case):
            trial = case[:i] + case[i + 1:]
            if differs(trial):
                case = trial
            else:
                i += 1
        return case
    if isinstance(case, tuple):
        parts = list(case)
        for j, p in enumerate(parts):
            if isinstance(p, list):
                parts[j] = shrink(p, lambda x, j=j: differs(tuple(parts[:j] + [x] + parts[j + 1:])))
        return tuple(parts)
    return case


def main():
    job = json.load(sys.stdin)
    suite = load_file(job["suite"], "hidden_suite")
    out = {}
    if job.get("coverage"):
        lines = set()

        def tracer(frame, event, arg):
            if frame.f_code.co_filename == "<solution>":
                lines.add(frame.f_lineno)
            return tracer
        sys.settrace(tracer)
        try:
            run_suite(load_source(job["source"]), suite)
        finally:
            sys.settrace(None)
        out["lines"] = sorted(lines)
    else:
        try:
            mod = load_source(job["source"])
            out["failed"] = run_suite(mod, suite)
        except Exception as e:
            out["failed"], out["load_error"] = ["<load>"], repr(e)
        if job.get("diff") and not out["failed"]:
            spec = load_file(job["spec"], "task_spec")
            out["diff"] = differential(spec, load_source(job["ref"], "reference"), mod, job.get("n", 300), job.get("seed", 1))
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
