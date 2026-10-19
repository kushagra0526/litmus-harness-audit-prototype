"""Chart for the README from out/heldout_first_run.json."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

t = json.load(open("out/heldout_first_run.json"))["totals"]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
v = [t["coverage_found"], t["gaps_found"]]
b = ax[0].bar(["line coverage\n(uncovered tagged line)", "mutation + differential\naudit"], v, color=["#c0504d", "#4f81bd"])
ax[0].set_title(f"Planted harness gaps found (of {t['planted_gaps']})", fontsize=10)
v2 = [0, t["over_found"]]
b2 = ax[1].bar(["line coverage", "rewrite audit"], v2, color=["#c0504d", "#4f81bd"])
ax[1].set_title(f"Over-specified tests found (of {t['over_specified']}); false flags {t['false_over']} of {t['fine_tests']}", fontsize=10)
for axis, bars, vals in ((ax[0], b, v), (ax[1], b2, v2)):
    for bar, x in zip(bars, vals):
        axis.text(bar.get_x() + bar.get_width() / 2, x, str(x), ha="center", va="bottom")
fig.suptitle("3 held-out assessment tasks (6 hidden suites), frozen in git, first run", fontsize=11)
fig.tight_layout()
fig.savefig("docs/result.png", dpi=130)
