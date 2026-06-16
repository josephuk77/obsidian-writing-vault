# FaithLog Decision Log

This file records user-approved project decisions so Codex does not rely on guesses later.

## Rules

- Every product, architecture, data, deployment, test-strategy, or resume-metric decision must come from the user.
- If Codex is unsure, Codex must ask before implementation.
- Record the decision date, context, options if relevant, the user's decision, and the implementation impact.

## Decisions

### 2026-06-16 - User Owns All Project Decisions

- Context: The user stated that Codex must not develop or implement based on guesses.
- Decision: All ambiguous or unusual decisions must be asked of the user before implementation.
- Impact: Codex must stop and ask before choosing product behavior, architecture, schema, deployment, test strategy, monitoring scope, resume metrics, or implementation tradeoffs.

### 2026-06-16 - Track Resume Metrics During Development

- Context: The project will be deployed and operated, and the user wants resume-ready quantitative evidence.
- Decision: Codex should record measurable project progress, tests, troubleshooting, and improvements in Markdown and Obsidian.
- Impact: Metrics are tracked in `docs/resume-metrics.md` and mirrored to the Obsidian FaithLog note.
