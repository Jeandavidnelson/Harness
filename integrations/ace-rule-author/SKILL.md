---
name: ace-rule-author
description: Convert human architecture constraints into auditable ACE/CNL candidates and structured deterministic harness mappings. Use when a user asks to formalize, compile, normalize, or review an architecture rule written in ordinary language, especially when MUST/MUST NOT semantics, direct versus transitive dependencies, ambiguity, or mapping to required_edge, forbidden_edge, required_path, or forbidden_path must be preserved.
---

# Architecture Rule Author

Treat ACE as an authoring layer, never as the PASS/FAIL engine. Do not modify `architecture/rules/rules.yaml` without explicit user approval and deterministic validation.

## Workflow

1. Preserve the original rule verbatim.
2. Classify intent as `REQUIRE`, `FORBID`, `ALLOW`, or `UNKNOWN`.
3. Return status `EXACT`, `NEEDS_CLARIFICATION`, or `UNSUPPORTED`.
4. Produce a short single-clause ACE candidate only when semantics are exact.
5. Produce a structured interpretation with source role, relation, directness, target role, and policy.
6. Resolve roles only from project mappings. Otherwise return `role_resolution: REQUIRED`.
7. Map to `required_edge`, `forbidden_edge`, `required_path`, or `forbidden_path` when exact and supported.
8. Run `arch-harness ace compile --text "..."` for the deterministic supported corpus. If APE exists, run `arch-harness ace validate <file>` and record its result.

## Ambiguity guard

Return `NEEDS_CLARIFICATION` and no ACE candidate when advisory or conditional language includes `should`, `normally`, `generally`, `preferably`, `when appropriate`, `where possible`, `if necessary`, `typically`, `ideally`, `recommended`, or `avoid`. Never harden these words into MUST or MUST NOT.

Preserve direct versus transitive meaning. “Directly call” maps to an edge. A general “depend on” maps to a path only when the statement clearly prohibits the dependency; otherwise request clarification.

## Required output

Return:

```yaml
original: <verbatim input>
intent: REQUIRE | FORBID | ALLOW | UNKNOWN
status: EXACT | NEEDS_CLARIFICATION | UNSUPPORTED
ace: <candidate or null>
structured: <mapping or null>
assumptions: []
harness_rule: <mapping or null>
role_resolution: RESOLVED | REQUIRED
reason: []
```

Keep all assumptions visible. Reject unsupported compound constraints instead of guessing. Log every experimental conversion in `logs/V1_1_ACE_VALIDATION_LOG.md`.

