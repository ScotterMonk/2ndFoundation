# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

The following is one stage in a multi-stage "application creation project". Do not stray into doing more than is set out here. If you have ideas that might involve additions:
1) Look at the other stages (`build_plan/stage-**.md`) to be sure they do not already cover the functionality.
2) If they do not, consult user.

## STAGE 04: USER INTERFACE / Application Pages & Flow
- Phase 1: Navigation Menu
- Phase 2: Page Descriptions
  - Home (/)
  - Search (/search)
  - Upload (/upload)
  - RL Task (/rl-task/*) - Core Assignment Interface
    - Overview
    - Submit
    - Results
    - History
  - Testing (/testing)
  - Admin (/admin)

Use `build_plan/app-summary.md`

References:
- `build_plan/ref-routes.md` - Implementation details for route handlers in routes/ folder
- `build_plan/ref-templates.md` - Base template structure and common patterns