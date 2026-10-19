"""Audit one hidden suite: what line coverage says vs what the mutation + rewrite audit finds."""
import sys

from harnessaudit.audit import audit

TASK, SUITE = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("tasks/dev/rate_limiter", "tests_weak.py")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    r = audit(TASK, SUITE)
    print(f"{TASK}/{SUITE}")
    print(f"  line coverage of the reference: {r['line_coverage']:.0%}   (what a coverage check reports)")
    print(f"  mutants: {r['mutants']}, killed {r['killed']}, equivalent (no difference on 300 random inputs) {len(r['equivalent'])}, "
          f"kill rate {r['kill_rate']:.0%}")
    print("\n  GAP: a submission with this bug passes every hidden test")
    for ln, ws in sorted(r["gaps"].items()):
        w = ws[0]
        print(f"    line {ln}: `{r['reference_lines'][ln - 1].strip().split('  #')[0]}`  [{w['op']}]")
        print(f"      input {w['case']}\n      reference -> {w['reference']}\n      buggy     -> {w['candidate']}")
    print("\n  OVER_SPECIFIED: fails a correct solution that is written differently")
    for t, why in sorted(r["over_specified"].items()):
        print(f"    {t}: {'; '.join(why)}")
