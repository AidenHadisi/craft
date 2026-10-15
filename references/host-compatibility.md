# Host compatibility

Use the current coding system's native tools for delegation, browsing, terminal work, and user questions. Inherit its configured model unless the user chooses another one.

Resolve Craft agent names against the available roles; some hosts prefix them with the plugin name (for example, `craft:craft-coder`). If a named role is unavailable but generic subagents exist, read the matching definition in `../agents/` and pass its full instructions and read-only constraint in the delegation brief. Give each agent the task context, owned files, constraints, and verification commands. If the host cannot delegate, explain that limitation before starting a workflow requiring independent review; do not silently replace independent review with self-review.

Respect read-only agent instructions across all tools, including shell commands and remote integrations. Platform tool restrictions supplement these instructions; they are not a universal read-only sandbox.

Use installed companion skills when available. Where a workflow provides a fallback, use it. If a required capability has no fallback, report what is missing rather than inventing a tool or claiming the step passed.
