---
name: architecture-rule-author
description: Derive explicit, reviewable architecture rule candidates from Mermaid diagrams and project intent without silently turning interpretation into blocking policy. Use when an agent must translate architecture diagrams or guidelines into architecture-harness rules, clarify ambiguous boundaries, revise candidate rules, or prepare rules for human validation.
---

# Architecture Rule Author

Convert diagrams into candidate policy while preserving the boundary between declared facts and validated rules. Never promote a rule or edit `architecture/rules/rules.yaml` without explicit human confirmation.

## Workflow

1. Run `arch-harness agent context --focus <relevant-node> --format json` for each relevant area. Read only the Mermaid files and guidelines needed for the request.
2. Identify declared components and directions. Treat Mermaid edges as `DECLARED`, not automatically as required or forbidden dependencies.
3. Form candidate constraints using only `required_edge`, `forbidden_edge`, `required_path`, or `forbidden_path`.
4. Ask concise clarification questions when intent changes policy. In particular, clarify whether an edge is mandatory or illustrative, whether indirect paths count, the scope, exceptions, and desired severity.
5. Write agreed drafts to `architecture/rules/candidates.yaml` with `status: candidate`. Use `provenance: GENERATED` unless the user explicitly confirms the exact rule, then use `USER_CONFIRMED` while keeping candidate status until review.
   Choose `applicability: when_observed` for future/optional code, `required` when missing mappings must be treated as configuration errors, or `declared_only` for guidance that must never be evaluated.
6. Validate syntax with `arch-harness rules validate --file architecture/rules/candidates.yaml`.
7. Present each rule with its rationale, assumptions, unresolved questions, and expected impact. Stop before promotion.
8. Only after explicit human approval, move the approved rule to `architecture/rules/rules.yaml`, set `status: validated`, record the decision in `architecture/rules/decisions.md`, refresh the graph when source changed, and run `arch-harness gate --format json`.

## Candidate schema

Include every field:

```yaml
- id: domain-must-not-depend-on-infrastructure
  type: forbidden_path
  source: Domain
  target: Infrastructure
  allowed_targets: []
  severity: error
  scope: [src/domain]
  exceptions: []
  rationale: Keep domain policy independent from technical adapters.
  provenance: GENERATED
  status: candidate
  applicability: when_observed
```

Define referenced roles with explicit `exact`, `prefix`, `suffix`, or `contains` matchers. Prefer `exact` for blocking rules. Never accept a source or target that resolves to nothing as evidence of compliance.

## Safety rules

- Keep all LLM interpretations non-blocking until human review.
- Do not infer a forbidden dependency merely because Mermaid omits an edge.
- Do not infer a required dependency merely because Mermaid shows an edge.
- Do not auto-resolve conflicting diagrams; report the conflict and ask.
- Do not modify application code while authoring policy.
- Do not place ArchUnit, dependency-cruiser, or another native validator inside the core. Recommend such tests separately after a rule is validated.

## Completion report

Report candidate count, clarification count, validation result, provenance of each candidate, and whether any rule was promoted. A successful authoring run may end with unresolved questions and zero promoted rules.
