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

5. Run `arch-harness --root /path/to/project doctor`, then inspect `_bmad/custom/*.toml` and commit them with the project.

The installer refuses to overwrite an existing override. Merge it manually or rerun with `--force` only after reviewing the replacement.

BMAD updates may change exposed fields. After an update, compare the installed `.agents/skills/<skill>/customize.toml` files with these overrides and use BMAD's resolver to verify the merge.
