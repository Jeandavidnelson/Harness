# V1.1 ACE Validation Log

APE availability: `UNAVAILABLE` at initial inspection. Absence is non-fatal and no parse result is invented.

## Rule conversion

### Human input
No controller may directly call a repository.

### Status
EXACT / FORBID

### ACE candidate
No controller may directly call a repository.

### APE validation
NOT_RUN — APE unavailable.

### Structured interpretation
`controller calls directly repository; forbidden`

### Assumptions
None. Project role resolution remains required.

### Harness mapping
`forbidden_edge Controller -> Repository`

### Final decision
ACCEPTED

## Rule conversion

### Human input
Every repository may access a database.

### Status
EXACT / ALLOW

### ACE candidate
Every repository may access a database.

### APE validation
NOT_RUN — APE unavailable.

### Structured interpretation
`repository accesses directly database; allowed`

### Assumptions
None. An ALLOW statement has no standalone V1 rule type.

### Harness mapping
Not available without an enclosing allowlist policy.

### Final decision
ACCEPTED as authoring output; not compiled into `rules.yaml`.

## Rule conversion

### Human input
No domain component may depend on infrastructure.

### Status
EXACT / FORBID

### ACE candidate
No domain component may depend on an infrastructure component.

### APE validation
NOT_RUN — APE unavailable.

### Structured interpretation
`domain depends_on transitively infrastructure; forbidden`

### Assumptions
Dependency is treated as transitive because the statement prohibits the dependency generally.

### Harness mapping
`forbidden_path Domain -> Infrastructure`

### Final decision
ACCEPTED

## Ambiguous corpus

The three advisory inputs containing `should`, `normally`, `preferably`, or conditional language all returned `NEEDS_CLARIFICATION`, `UNKNOWN`, no ACE candidate, and no harness mapping.

### Final decision
NEEDS_CLARIFICATION — none were hardened.

