# craft-watch — design notes

Why the skill is shaped the way it is. The skill itself is the reference; this is just the reasoning behind the decisions, kept for whoever changes it later.

## The shape

One skill, one file per feature, no modes. `/craft-watch <feature>` is a linear setup procedure run once: learn the feature, write `docs/watch/<feature>.md`, put it on an automation.

The file is self-executing — it carries the checks, how to read them, and the log — so scheduling it is a cron trigger whose entire prompt is `Run the watch at docs/watch/<feature>.md`. That's why the skill has no "run" mode: the run instructions belong with the file, since a scheduled cloud agent wakes up with the file and nothing else. Keeping them there also means the run logic lives in one place, and a feature's reporting can be tuned by editing that feature's file rather than the plugin.

## The decisions

**Discovery is expensive and happens once; runs are cheap and repeat.** Every system that does this well splits the two. Letting an agent re-derive what matters on every run is both costly and non-comparable — you can't diff run N against run N−1 if it asked different questions each time.

**Checks are proven before they're written down.** A query nobody has run is a guess. Running it also produces the "normal" line, so the baseline is an observed value rather than an invented threshold. This is the step that would be most tempting to skip when the agent already has the feature in context, so the skill calls it non-skippable.

**An empty result is a broken check, not a pass.** This is how these systems die quietly: a column gets renamed, the query stops matching, and the watch reports healthy forever.

**Two tiers: fixed checks, then look around.** The fixed checks give comparability across runs; the look-around gives a shot at what nobody enumerated. Neither alone works — pure exploration produces a different answer every run and no baseline, a pure checklist goes blind the moment reality does something new. The run may propose new checks in its log entry but never edits the check list itself.

**Two kinds of finding: problems and observations.** The second is easy to design away by accident. A watch that only reports failures tells you the feature is alive; one that also reports observations — a step eating the runtime, output weak for one kind of input, a mistuned retry limit, a path nobody takes — is how it gets better. So the bar is *would a person want to know this*, not *is something broken*, while still requiring that the log doesn't already say it.

**"Nothing new" is the expected output.** An agent that finds something interesting every single run gets muted within two weeks. Most runs should produce one line.

**No plan document required.** The skill uses whatever context it has and reads the code for the rest, so it works on something that shipped years ago from a cold session. The craft integration is an optional shortcut, not a dependency.

**Read-only, enforced below the prompt.** The instruction matters, but the real enforcement is a `GRANT SELECT`-only role on a read replica with a statement timeout. Worth knowing that `beforeMCPExecution` hooks don't run on Cloud Agents, so under a cloud schedule the DB grant is doing all the actual work.

**Production logs are untrusted input.** A log line containing instruction-shaped text is a prompt injection into a file the agent reads on every future run. The log section holds the agent's own prose only — error strings quoted short and inline, never dumped.

**GitHub issue as the notification.** It's the one channel that needs nothing beyond the git provider a cloud agent already requires, and it emails and pushes for free. Cursor Automations have no email or notify action, and the `sessionStart` hook that could surface an unread report drops its context on a known race.

## Deliberately left out

Fingerprint algorithms, separate state files, statistical significance testing, severity tiers, recomputed baselines, snapped time windows. All standard in mature monitoring, all a response to scale this doesn't have — a handful of findings a week, judged by an agent reading a short log. Add one only when the simple version visibly breaks: fingerprints if it starts repeating itself, snapped windows if you start chasing phantom day-over-day deltas, recomputed baselines if seasonality causes false positives.
