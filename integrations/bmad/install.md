# Installation

1. Install Architecture Harness in the target project environment.
2. Install BMAD 6.11 or later:

   ```bash
   npx bmad-method install --modules bmm --tools codex
   ```

3. Install `uv`; BMAD 6.11 reports that `bmad-build` and `bmad-build-auto` halt without it.
4. From this repository, copy the reviewed team overrides into the BMAD project:

   ```bash
   arch-harness --root /path/to/project integrations install bmad --adapter-root /path/to/architecture-harness
   ```

5. Inspect the installed assets and commit them with the project.

   On a greenfield project with no source graph yet, verify the installed files first and run `doctor` only after the first `graph refresh`:

   ```bash
   test -f _bmad/custom/bmad-architecture.toml
   test -f _bmad/custom/bmad-build.toml
   test -f _bmad/custom/bmad-code-review.toml
   test -f .agents/skills/architecture-rule-author/SKILL.md
   test -f .agents/skills/architecture-rule-author/agents/openai.yaml
   rg -n "arch-harness" _bmad/custom/*.toml
   ```

   The installer JSON must report `"status": "PASS"`, `"integration": "bmad"`, `"core_dependency_added": false`, and five installed files.

6. After the first source code exists, verify the end-to-end integration:

   ```bash
   arch-harness --root /path/to/project graph refresh --format json
   arch-harness --root /path/to/project agent doctor --format json
   arch-harness --root /path/to/project gate --format json
   ```

   All three commands must return exit code 0. A gate PASS validates the architecture integration, not the application behavior; keep functional tests and code review.

The installer refuses to overwrite an existing override. Merge it manually or rerun with `--force` only after reviewing the replacement.

BMAD updates may change exposed fields. After an update, compare the installed `.agents/skills/<skill>/customize.toml` files with these overrides and use BMAD's resolver to verify the merge.
