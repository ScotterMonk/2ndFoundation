# Plan: Consolidate AGENTS.md Files (Refined in Planner-b)

- Short plan name: 251025_consolidate_agents_files
- Plan file: `.roo/docs/plans/plan_251025_consolidate_agents_files.md`
- Autonomy level: High
- Project size: Multi-Phase (one phase per mode)
- Testing type: No testing (documentation-only change)
- Preferred modes to delegate to:
    - `/task-simple`: Small ops/tasks.
    - `/code-monkey`: Coding, analysis, following instructions.

Objective:
Create a single source of truth for project-specific technical guidance in `agents.md`, reduce duplication across mode folders, and keep `01-general.md` focused on cross-mode behavioral standards.

Single source of truth boundaries:
- `agents.md` = Project technical knowledge and patterns (what and how)
- `01-general.md` = Cross-mode behavioral standards and global workflow rules (how to work)
- Mode files (eg, `.roo/rules-code/01-code.md`) = Mode role/scope and workflow (when to use, how to escalate), linking back to `agents.md` for technicals

Backups and archival:
- Any deleted/moved doc is first copied to `.roo/docs/old_versions/[file name]_[yyyy-mm-dd_hhmmss]`
- Replace content with minimal link-forward stubs where removal might surprise readers

---

Foundation: Known overlaps and target landing sections in master
- Naming Conventions → Section in `agents.md` named “Naming Conventions”
- Code Standards (comment headers, modularization limits, spacing, SQL strings, file operations) → “Code Standards”
- Browser Testing (tooling, workflow, auth strategy, tokens) → “Browser Testing”
- Documentation paths (backups, plans_completed, schema changes) → “Documentation”
- External API Provider framework (BaseApiProvider, descriptors, configuration) → “External API Provider Framework”
- Environment & Commands (Windows/PowerShell, `python app.py`, `.\activate.ps1`, no Linux commands) → “Environment & Run Commands”

Note on tester-specific content:
- Cross-project testing heuristics and browser automation rules: centralize in `agents.md`
- Mode-specific tester workflow (what tester mode does, escalation rules): keep in `.roo/rules-tester/01-tester.md`

---

Phase 0: Normalize cross-file roles (01-general.md vs agents.md)
Goal:
- Ensure `01-general.md` contains behavioral standards and global workflow only, and references `agents.md` for technical sections.
Inputs:
- `.roo/rules/01-general.md`
- `agents.md`
Actions (high level):
- Remove duplicated technical specifics from `01-general.md` (detailed browser testing steps, extended naming/code standards already present in `agents.md`)
- Add explicit cross-reference lines to `agents.md` for Naming Conventions, Code Standards, Browser Testing procedures
Acceptance criteria:
- `01-general.md` contains only cross-mode behavioral standards, global workflows, and summary pointers to `agents.md`
- No detailed browser testing procedures remain in `01-general.md`
- Link stubs like: “See `agents.md` → Browser Testing” are present

---

Phase 1: Consolidate /code mode (source: `.roo/rules-code/AGENTS.md`)
Goal:
- Merge any unique technical guidance into master `agents.md` and delete the mode-specific AGENTS.md
Inputs:
- `.roo/rules-code/AGENTS.md`
- `agents.md`
Expected landing sections:
- Naming Conventions
- Code Standards
- Environment & Run Commands (de-duplicate)
Acceptance criteria:
- All unique technical details are represented under proper sections in `agents.md`
- `.roo/rules-code/AGENTS.md` archived then deleted
- `.roo/rules-code/01-code.md` references `agents.md` for project standards and keeps only role/workflow

---

Phase 2: Consolidate /code-monkey mode (source: `.roo/rules-code-monkey/AGENTS.md`)
Goal:
- Merge unique technical guidance into master and delete mode AGENTS.md
Inputs:
- `.roo/rules-code-monkey/AGENTS.md`
- `agents.md`
Expected landing sections:
- Naming Conventions
- Code Standards (emphasis on atomicity, simple implementations)
Acceptance criteria:
- Unique technical details are in `agents.md`
- `.roo/rules-code-monkey/AGENTS.md` archived then deleted
- `.roo/rules-code-monkey/01-code-monkey.md`: keep only role, when to use, and escalation; link to `agents.md` for standards

---

Phase 3: Consolidate /debug mode (source: `.roo/rules-debug/AGENTS.md`)
Goal:
- Merge unique technical guidance into master and delete mode AGENTS.md
Inputs:
- `.roo/rules-debug/AGENTS.md`
- `agents.md`
Expected landing sections:
- Environment & Run Commands (no Linux), Browser Testing safety notes, Documentation paths
- If present, any common debugging heuristics that apply across modes
Acceptance criteria:
- Unique technical content is centralized in `agents.md`
- `.roo/rules-debug/AGENTS.md` archived then deleted
- `.roo/rules-debug/01-debug.md`: retain role, scope, escalation; link `agents.md` for technical references

---

Phase 4: Consolidate /front-end mode (source: `.roo/rules-front-end/AGENTS.md`)
Goal:
- Merge unique technical guidance into master and delete mode AGENTS.md
Inputs:
- `.roo/rules-front-end/AGENTS.md`
- `agents.md`
Expected landing sections:
- Code Standards (templating: jinja-html)
- Naming Conventions (component/template naming if present)
- Browser Testing references (UI)
Acceptance criteria:
- Unique content reflected in `agents.md`
- `.roo/rules-front-end/AGENTS.md` archived then deleted
- `.roo/rules-front-end/01-front-end.md`: keep role and workflow; link `agents.md`

---

Phase 5: Consolidate /tester mode (source: `.roo/rules-tester/AGENTS.md`)
Goal:
- Merge tester-specific reusable technical guidance into master and delete mode AGENTS.md, while preserving tester workflow in `01-tester.md`
Inputs:
- `.roo/rules-tester/AGENTS.md`
- `.roo/rules-tester/01-tester.md`
- `agents.md`
Expected landing sections:
- Browser Testing (tool actions, constraints, auth strategy, token optimization, **screenshot quality: 45-60%, default: 70%**)
- **Testing Guidance (cross-project "what to test" heuristics, code patterns to test)**
- Documentation (plans_completed, schema log) remain referenced
Acceptance criteria:
- Cross-project tester guidance incorporated into `agents.md` under Browser Testing and Testing Guidance
- `.roo/rules-tester/AGENTS.md` archived then deleted
- `.roo/rules-tester/01-tester.md` retains tester-specific workflow, escalation, and references `agents.md` for technicals

---

Phase 6: Finalize master `agents.md` structure and clarity
Goal:
- Ensure `agents.md` is complete, concise, and logically organized
Proposed section order:
1) Environment & Run Commands
2) Critical Non-Standard Patterns
3) Naming Conventions
4) Code Standards
5) **Testing Guidance**
6) Browser Testing (preconditions, actions, workflow rules, auth strategy, token optimization, safety)
7) Documentation
8) External API Provider Framework
9) Configuration
Acceptance criteria:
- No duplicate paragraphs across sections
- All cross-references (eg, from mode docs and `01-general.md`) resolve to a single clear section
- Read-through shows smooth flow and minimal redundancy

---

Phase 7: Update mode workflow docs and references
Goal:
- Simplify each mode’s `01-*.md` to focus on role, when to use, workflow, and escalation; reference `agents.md` for technical standards
Inputs:
- `.roo/rules-code/01-code.md`, `.roo/rules-code-monkey/01-code-monkey.md`, `.roo/rules-front-end/01-front-end.md`, `.roo/rules-debug/01-debug.md`, `.roo/rules-tester/01-tester.md`
Acceptance criteria:
- Each mode `01-*.md` deletes any duplicated technical standards and uses “See `agents.md` → <Section>”
- All links verified to be valid
- Tone and structure consistent across modes

---

Phase 8: Validation & cleanup
Goal:
- Validate that the repo no longer contains mode-specific AGENTS.md files and that references point to `agents.md`
Checks:
- Search repo for `AGENTS.md` under `.roo/rules-*/AGENTS.md` — none remain
- Verify `01-general.md` references sections in `agents.md` instead of repeating them
- Verify `agents.md` covers all target sections listed in this plan
- Ensure backups exist in `.roo/docs/old_versions/` for each removed file
Acceptance criteria:
- All checks pass
- Single source of truth is enforced

---

Risks and mitigations
- Risk: Losing mode-unique nuance during consolidation
  - Mitigation: Preserve mode-specific workflows in `01-*.md`, centralize only cross-project technical guidance
- Risk: Conflicts between duplicated/variant versions
  - Mitigation: Prefer the master `agents.md` voice/tone; integrate missing details; remove older conflicting statements
- Risk: Broken references after deletion
  - Mitigation: Replace deletions with stubs during commit; verify links in Phase 8

Hand-off to `/planner-c`
- Generate detailed atomic tasks per phase:
  - Each task = one atomic action
  - Include file paths, exact sections to edit, explicit acceptance criteria, and backup steps
  - Respect repository standards for backups and links

Primary files
- `agents.md`
- `.roo/rules/01-general.md`
- `.roo/rules-code/AGENTS.md`
- `.roo/rules-code/01-code.md`
- `.roo/rules-code-monkey/AGENTS.md`
- `.roo/rules-code-monkey/01-code-monkey.md`
- `.roo/rules-debug/AGENTS.md`
- `.roo/rules-debug/01-debug.md`
- `.roo/rules-front-end/AGENTS.md`
- `.roo/rules-front-end/01-front-end.md`
- `.roo/rules-tester/AGENTS.md`
- `.roo/rules-tester/01-tester.md`
- `.roo/docs/old_versions/` (backups)
## Detailed Atomic Tasks (Planner-c)

Conventions:
- Each task = one atomic action
- Mode hint: suggested execution mode for `/orchestrator`
- Integration points: files to touch
- Acceptance: clear, verifiable outcome

Phase 0: Normalize `01-general.md` vs `agents.md`
- Action: Copy `.roo/rules/01-general.md` to backups folder with timestamped name
  Mode hint: task-simple
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md), [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: A new file exists at `.roo/docs/old_versions/01-general.md_[yyyy-mm-dd_hhmmss].md`
- Action: Copy `agents.md` to backups folder with timestamped name
  Mode hint: task-simple
  Integration points: `@/agents.md`, [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: A new file exists at `.roo/docs/old_versions/agents.md_[yyyy-mm-dd_hhmmss].md`
- Action: Remove the detailed "Browser Testing" procedures section from `.roo/rules/01-general.md` (preconditions, actions, workflow rules, auth strategy, token optimization)
  Mode hint: code
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md)
  Acceptance: No "Browser Testing" subsections remain in `01-general.md`
- Action: Insert a single cross-reference line in `01-general.md` under Testing: “See `agents.md` → Browser Testing”
  Mode hint: code
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md), `@/agents.md`
  Acceptance: New line present and clickable link works to Browser Testing section in `agents.md`
- Action: Insert a cross-reference block at the top of “Standards” in `01-general.md`: “See `agents.md` → Naming Conventions; Code Standards; Browser Testing”
  Mode hint: code
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md), `@/agents.md`
  Acceptance: Cross-reference block exists and all three links resolve
- Action: Normalize existing references in `01-general.md` from back-ticked file mentions to clickable file links (eg, change plain `@/agents.md` reference to `@/agents.md`
  Mode hint: code
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md)
  Acceptance: All file references in `01-general.md` are clickable link format per project rule
- Action: Search `01-general.md` for the string "Browser Testing" to verify no stepwise procedures remain
  Mode hint: task-simple
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md)
  Acceptance: Only the cross-reference line remains; no procedure blocks found

Phase 1: Consolidate `/code` mode (source: `.roo/rules-code/AGENTS.md`)
- Action: Copy `.roo/rules-code/AGENTS.md` to backups folder with timestamped name
  Mode hint: task-simple
  Integration points: [.roo/rules-code/AGENTS.md](.roo/rules-code/AGENTS.md), [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: Backup present in `old_versions`
- Action: Read `.roo/rules-code/AGENTS.md` to identify unique technical content not already in `agents.md`
  Mode hint: ask
  Integration points: [.roo/rules-code/AGENTS.md](.roo/rules-code/AGENTS.md), `@/agents.md`
  Acceptance: A short comparison note recorded in commit message or plan log indicating what was unique
- Action: Append the unique entries under the appropriate section(s) in `agents.md` (Naming Conventions or Code Standards)
  Mode hint: code
  Integration points: `@/agents.md`
  Acceptance: New lines added in correct sections; wording aligns with `agents.md` tone; links valid
- Action: Delete `.roo/rules-code/AGENTS.md`
  Mode hint: task-simple
  Integration points: [.roo/rules-code/AGENTS.md](.roo/rules-code/AGENTS.md)
  Acceptance: File no longer exists in repo
- Action: Edit `.roo/rules-code/01-code.md` to remove duplicated technical standards and add “See `agents.md` → Naming Conventions; Code Standards”
  Mode hint: docs-writer
  Integration points: [.roo/rules-code/01-code.md](.roo/rules-code/01-code.md), `@/agents.md`
  Acceptance: File focuses on role/scope/workflow; includes link to `agents.md` sections

Phase 2: Consolidate `/code-monkey` mode (source: `.roo/rules-code-monkey/AGENTS.md`)
- Action: Copy `.roo/rules-code-monkey/AGENTS.md` to backups with timestamp
  Mode hint: task-simple
  Integration points: [.roo/rules-code-monkey/AGENTS.md](.roo/rules-code-monkey/AGENTS.md), [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: Backup present
- Action: Read `.roo/rules-code-monkey/AGENTS.md` to identify unique technical content not in `agents.md`
  Mode hint: ask
  Integration points: [.roo/rules-code-monkey/AGENTS.md](.roo/rules-code-monkey/AGENTS.md), `@/agents.md`
  Acceptance: Brief comparison recorded
- Action: Append unique entries into `agents.md` under Code Standards (atomicity focus) or Naming Conventions as appropriate
  Mode hint: code
  Integration points: `@/agents.md`
  Acceptance: Content merged cleanly; no duplicates introduced
- Action: Delete `.roo/rules-code-monkey/AGENTS.md`
  Mode hint: task-simple
  Integration points: [.roo/rules-code-monkey/AGENTS.md](.roo/rules-code-monkey/AGENTS.md)
  Acceptance: File removed
- Action: Edit `.roo/rules-code-monkey/01-code-monkey.md` to point to `agents.md` sections and remove project standards content
  Mode hint: docs-writer
  Integration points: [.roo/rules-code-monkey/01-code-monkey.md](.roo/rules-code-monkey/01-code-monkey.md), `@/agents.md`
  Acceptance: Document focuses on role/workflow/escalation; includes proper cross-references

Phase 3: Consolidate `/debug` mode (source: `.roo/rules-debug/AGENTS.md`)
- Action: Copy `.roo/rules-debug/AGENTS.md` to backups with timestamp
  Mode hint: task-simple
  Integration points: [.roo/rules-debug/AGENTS.md](.roo/rules-debug/AGENTS.md), [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: Backup present
- Action: Read `.roo/rules-debug/AGENTS.md` to identify unique technical content for centralization (env constraints, safety notes)
  Mode hint: ask
  Integration points: [.roo/rules-debug/AGENTS.md](.roo/rules-debug/AGENTS.md), `@/agents.md`
  Acceptance: Comparison recorded
- Action: Append unique entries into `agents.md` under Environment & Run Commands or Browser Testing safety notes
  Mode hint: code
  Integration points: `@/agents.md`
  Acceptance: Content merged without duplication; safety note preserved
- Action: Delete `.roo/rules-debug/AGENTS.md`
  Mode hint: task-simple
  Integration points: [.roo/rules-debug/AGENTS.md](.roo/rules-debug/AGENTS.md)
  Acceptance: File removed
- Action: Edit `.roo/rules-debug/01-debug.md` to reference `agents.md` sections for technical standards
  Mode hint: docs-writer
  Integration points: [.roo/rules-debug/01-debug.md](.roo/rules-debug/01-debug.md), `@/agents.md`
  Acceptance: Role/workflow retained; technical details delegated to `agents.md`

Phase 4: Consolidate `/front-end` mode (source: `.roo/rules-front-end/AGENTS.md`)
- Action: Copy `.roo/rules-front-end/AGENTS.md` to backups with timestamp
  Mode hint: task-simple
  Integration points: [.roo/rules-front-end/AGENTS.md](.roo/rules-front-end/AGENTS.md), [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: Backup present
- Action: Read `.roo/rules-front-end/AGENTS.md` to isolate unique front-end technical guidance (eg, jinja-html reinforcement)
  Mode hint: ask
  Integration points: [.roo/rules-front-end/AGENTS.md](.roo/rules-front-end/AGENTS.md), `@/agents.md`
  Acceptance: Comparison recorded
- Action: Append unique entries into `agents.md` under Code Standards (templating: jinja-html)
  Mode hint: code
  Integration points: `@/agents.md`
  Acceptance: Content merged correctly
- Action: Delete `.roo/rules-front-end/AGENTS.md`
  Mode hint: task-simple
  Integration points: [.roo/rules-front-end/AGENTS.md](.roo/rules-front-end/AGENTS.md)
  Acceptance: File removed
- Action: Edit `.roo/rules-front-end/01-front-end.md` to reference `agents.md` standards
  Mode hint: docs-writer
  Integration points: [.roo/rules-front-end/01-front-end.md](.roo/rules-front-end/01-front-end.md), `@/agents.md`
  Acceptance: File contains role/workflow; standards link to `agents.md`

Phase 5: Consolidate `/tester` mode (source: `.roo/rules-tester/AGENTS.md`)
- Action: Copy `.roo/rules-tester/AGENTS.md` to backups with timestamp
  Mode hint: task-simple
  Integration points: [.roo/rules-tester/AGENTS.md](.roo/rules-tester/AGENTS.md), [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: Backup present
- Action: Read `.roo/rules-tester/AGENTS.md` to identify cross-project testing guidance to centralize (browser_action workflow, auth strategy, token optimization)
  Mode hint: ask
  Integration points: [.roo/rules-tester/AGENTS.md](.roo/rules-tester/AGENTS.md), `@/agents.md`
  Acceptance: Comparison recorded
- Action: Append the "Code Patterns to Test" section from `.roo/rules-tester/AGENTS.md` into `agents.md` under a new "Testing Guidance" section.
   Mode hint: code
   Integration points: `@/agents.md`, [.roo/rules-tester/AGENTS.md](.roo/rules-tester/AGENTS.md)
   Acceptance: New "Testing Guidance" section exists in `agents.md` with the "Code Patterns to Test" content.
- Action: Append tester-agnostic guidance into `agents.md` under Browser Testing, specifically resolving the screenshot quality discrepancy to 45-60%, default: 70%.
   Mode hint: code
   Integration points: `@/agents.md`, [.roo/rules-tester/AGENTS.md](.roo/rules-tester/AGENTS.md)
   Acceptance: Browser Testing section in `agents.md` reflects the reconciled screenshot quality.
- Action: Delete `.roo/rules-tester/AGENTS.md`
  Mode hint: task-simple
  Integration points: [.roo/rules-tester/AGENTS.md](.roo/rules-tester/AGENTS.md)
  Acceptance: File removed
- Action: Edit `.roo/rules-tester/01-tester.md` to preserve tester-specific workflow and reference `agents.md` for technical procedures
  Mode hint: docs-writer
  Integration points: [.roo/rules-tester/01-tester.md](.roo/rules-tester/01-tester.md), `@/agents.md`
  Acceptance: File focuses on role/workflow; technicals delegated to `agents.md`

Phase 6: Finalize structure of `agents.md`
- Action: Reorder sections in `agents.md` to: Environment & Run Commands; Critical Non-Standard Patterns; Naming Conventions; Code Standards; Testing Guidance; Browser Testing; Documentation; External API Provider Framework; Configuration
   Mode hint: docs-writer
   Integration points: `@/agents.md`
   Acceptance: Sections appear in specified order
- Action: Normalize headings and subheadings in `agents.md` to consistent style and capitalization
  Mode hint: docs-writer
  Integration points: `@/agents.md`
  Acceptance: All headers consistent; table of contents (if present) remains accurate
- Action: Ensure each section header in `agents.md` is linkable; add anchor-compatible headings if required
  Mode hint: docs-writer
  Integration points: `@/agents.md`
  Acceptance: Intra-doc links and external references to these sections resolve

Phase 7: Update mode workflow docs to reference `agents.md`
- Action: Edit `.roo/rules-code/01-code.md` to add “Project Standards” paragraph linking to `agents.md` sections and remove any duplicated standards
  Mode hint: docs-writer
  Integration points: [.roo/rules-code/01-code.md](.roo/rules-code/01-code.md), `@/agents.md`
  Acceptance: Role/workflow only; standards link present
- Action: Edit `.roo/rules-code-monkey/01-code-monkey.md` to add “Project Standards” paragraph linking to `agents.md` sections and remove duplicates
  Mode hint: docs-writer
  Integration points: [.roo/rules-code-monkey/01-code-monkey.md](.roo/rules-code-monkey/01-code-monkey.md), `@/agents.md`
  Acceptance: Role/workflow only; standards link present
- Action: Edit `.roo/rules-debug/01-debug.md` to add “Project Standards” paragraph linking to `agents.md` sections and remove duplicates
  Mode hint: docs-writer
  Integration points: [.roo/rules-debug/01-debug.md](.roo/rules-debug/01-debug.md), `@/agents.md`
  Acceptance: Role/workflow only; standards link present
- Action: Edit `.roo/rules-front-end/01-front-end.md` to add “Project Standards” paragraph linking to `agents.md` sections and remove duplicates
  Mode hint: docs-writer
  Integration points: [.roo/rules-front-end/01-front-end.md](.roo/rules-front-end/01-front-end.md), `@/agents.md`
  Acceptance: Role/workflow only; standards link present
- Action: Edit `.roo/rules-tester/01-tester.md` to add “Project Standards” paragraph linking to `agents.md` sections and remove duplicates
  Mode hint: docs-writer
  Integration points: [.roo/rules-tester/01-tester.md](.roo/rules-tester/01-tester.md), `@/agents.md`
  Acceptance: Role/workflow only; standards link present

Phase 8: Validation & cleanup
- Action: Search repo for any remaining `AGENTS.md` under `.roo/rules-*` directories
  Mode hint: task-simple
  Integration points: [.roo/rules-code/](.roo/rules-code/), [.roo/rules-code-monkey/](.roo/rules-code-monkey/), [.roo/rules-front-end/](.roo/rules-front-end/), [.roo/rules-debug/](.roo/rules-debug/), [.roo/rules-tester/](.roo/rules-tester/)
  Acceptance: No `AGENTS.md` remain in mode directories
- Action: Verify backups exist in `.roo/docs/old_versions/` for each removed `AGENTS.md`
  Mode hint: task-simple
  Integration points: [.roo/docs/old_versions/](.roo/docs/old_versions/)
  Acceptance: One timestamped backup per removed file found
- Action: Verify `.roo/rules/01-general.md` contains only behavioral standards and cross-references (no detailed Browser Testing procedures)
  Mode hint: task-simple
  Integration points: [.roo/rules/01-general.md](.roo/rules/01-general.md)
  Acceptance: File passes inspection; only references remain
- Action: Skim `agents.md` to confirm all targeted sections exist and cross-references from mode docs resolve
  Mode hint: task-simple
  Integration points: `@/agents.md`, [.roo/rules-*/01-*.md](.roo/rules-code/01-code.md)
  Acceptance: All links are clickable and correct

Notes for executors:
- When archiving, retain original filename + "_[yyyy-mm-dd_hhmmss]"
- Maintain voice/tone of `agents.md` when merging unique statements
- Do not move mode-specific workflows into `agents.md`; keep them in `01-*.md`