---
name: architecture-rule-author
description: Automatically translate official-parser-validated Mermaid diagrams into declared facts, Graphify-backed role mappings, and reviewable Architecture Harness rule candidates. Use when an orchestrator creates or changes architecture, after the first greenfield code graph exists, when mappings are unresolved, or when rules need human promotion without silently turning LLM interpretation into blocking policy.
---

# Architecture Rule Author

Convert diagrams into candidate policy while preserving the boundary between declared facts and validated rules. Never promote a rule or edit `architecture/rules/rules.yaml` without explicit human confirmation.

## Workflow

1. Run `arch-harness rules author-context --format json`. This required input contains official Mermaid diagram types, complete validated source, normalized facts, and ranked Graphify mapping proposals.
2. Process every Mermaid file and retain every meaningful declared element. For a diagram without graph-like edges, preserve its facts as `declared_only` guidance or rationale instead of discarding it.
3. Resolve mappings automatically. Accept a `resolved_candidate` only after checking its Graphify id, file, symbol kind and diagram meaning. For `ambiguous`, choose when one candidate is clearly correct; ask the human only when multiple meanings remain plausible. For `pending_code`, emit `when_observed` and rerun after the first Graphify refresh.
4. Form candidate constraints using only `required_edge`, `forbidden_edge`, `required_path`, or `forbidden_path`. Treat Mermaid edges as `DECLARED`, not automatically as required or forbidden dependencies.
5. Ask concise clarification questions only when the answer changes policy and cannot be derived from Mermaid, guidelines, observed code, or existing decisions. Distinguish mandatory versus illustrative, direct versus transitive, scope, exceptions, and severity.
6. Write all drafts and resolved role matchers to `architecture/rules/candidates.yaml` with `status: candidate`. Use `provenance: GENERATED` unless the user explicitly confirms the exact rule, then use `USER_CONFIRMED` while keeping candidate status until review.
   Choose `applicability: when_observed` for future/optional code, `required` when missing mappings must be treated as configuration errors, or `declared_only` for guidance that must never be evaluated.
7. Validate syntax with `arch-harness rules validate --file architecture/rules/candidates.yaml`. Never claim a mapping is resolved unless its matcher resolves an observed Graphify node.
8. Present each rule with its rationale, mapping evidence, assumptions, unresolved questions, and expected impact. Stop before promotion.
9. Only after explicit human approval, move the approved rule to `architecture/rules/rules.yaml`, set `status: validated`, record the decision in `architecture/rules/decisions.md`, refresh the graph when source changed, and run `arch-harness gate --format json`.

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

For each automatically resolved role, include its observed id in the matcher and cite the Graphify file in the completion report. Do not invent node ids from Mermaid names.

## Safety rules

- Keep all LLM interpretations non-blocking until human review.
- Do not infer a forbidden dependency merely because Mermaid omits an edge.
- Do not infer a required dependency merely because Mermaid shows an edge.
- Do not auto-resolve conflicting diagrams; report the conflict and ask.
- Do not modify application code while authoring policy.
- Do not place ArchUnit, dependency-cruiser, or another native validator inside the core. Recommend such tests separately after a rule is validated.

## Completion report

Report Mermaid file/type count, declared facts retained, candidate count, resolved/ambiguous/pending mappings, clarification count, validation result, provenance of each candidate, and whether any rule was promoted. A successful authoring run may end with unresolved questions and zero promoted rules.
