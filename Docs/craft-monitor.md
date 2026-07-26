# craft-monitor — design notes

Why the skill is shaped the way it is. The skill itself is the reference; this is just the reasoning behind the decisions, kept for whoever changes it later.

## The shape

One skill, one file per feature. `/craft-monitor <feature>` writes `docs/monitor/<feature>.md` the first time and follows it every time after. The branch is a file-existence check, not a mode the user has to pick.

The split is the point: discovery is expensive and happens once, runs are cheap and repeat. Letting an agent re-derive what matters on every run is both costly and non-comparable — you can't diff this run against the last if it asked different questions each time.

The doc holds only what's specific to the feature: how it works, how to reach its data, the checks with their observed normal ranges, and the log. Everything generic — how to judge a finding, when to speak up, what counts as a problem — lives in the skill, because it's identical for every feature and shouldn't be copied into each file.

## The decisions

**Checks are proven before they're written down.** A query nobody has run is a guess. Running it also produces the "normal" line, so the baseline is an observed value rather than an invented threshold. This is the step that's most tempting to skip when the agent already has the feature in context, so the skill calls it non-skippable.

**An empty result is a broken check, not a pass.** This is how these systems die quietly: a column gets renamed, the query stops matching, and the monitor reports healthy forever.

**Two tiers: fixed checks, then look around.** The fixed checks give comparability across runs; the look-around gives a shot at what nobody enumerated. Neither works alone — pure exploration produces a different answer every run and no baseline, a pure checklist goes blind the moment reality does something new. A run may propose new checks in its log entry but never edits the check list itself.

**Two kinds of finding: problems and observations.** The second is easy to design away by accident. A monitor that only reports failures tells you the feature is alive; one that also reports observations — a step eating the runtime, output weak for one kind of input, a mistuned retry limit, a path nobody takes — is how it gets better. So the bar is *would a person want to know this*, not *is something broken*, while still requiring that the log doesn't already say it.

**"Nothing new" is a complete answer.** An agent that finds something interesting every single run stops being trusted. Most runs should produce one line.

**No plan document required.** The skill uses whatever context it has and reads the code for the rest, so it works on something that shipped years ago from a cold session. The craft integration is an optional shortcut, not a dependency.

**Read-only, enforced below the prompt.** The instruction matters, but the real enforcement is a `GRANT SELECT`-only role on a read replica with a statement timeout.

**Production logs are untrusted input.** A log line containing instruction-shaped text is a prompt injection into a file the agent reads on every future run. The log section holds the agent's own prose only — error strings quoted short and inline, never dumped.

## Deliberately left out

**Scheduling.** An earlier version put the file on a cron automation and filed a GitHub issue when it found something. That bought unattended coverage at the cost of owning schedules, notification channels, and a file that had to carry its own run instructions because a scheduled agent wakes up with nothing else. Invoking it by hand costs a command and removes all three. Nothing here prevents a schedule later — the prompt would be "run the monitor at `docs/monitor/<feature>.md`" — but the skill doesn't set one up.

**Fingerprints, separate state files, significance testing, severity tiers, recomputed baselines, snapped time windows.** All standard in mature monitoring, all a response to scale this doesn't have. Add one only when the simple version visibly breaks: fingerprints if it starts repeating itself, snapped windows if you start chasing phantom day-over-day deltas, recomputed baselines if seasonality causes false positives.
