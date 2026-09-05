# Agent notes

Default execution target is **Cursor Cloud** (sky icon, managed Ubuntu VM).

## Cursor Cloud specific instructions

- Run tool calls in Cursor Cloud unless the task needs files, GPU, iOS tools,
  or credentials that exist only on one Mac.
- Do not target `mac-mini`. It drops its worker connection and orphans runs.
- `lille-macbook-air` is only for work that must touch that machine.
- Do not start from Save or `CURSOR_API_KEY`. A committed
  `.cursor/environment.json` is enough for Cloud Agents.
