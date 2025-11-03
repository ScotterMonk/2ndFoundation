# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

The following is one stage in a multi-stage "application creation project". Do not stray into doing more than is set out here. If you have ideas that might involve additions:
1) Look at the other stages (`build_plan/stage-**.md`) to be sure they do not already cover the functionality.
2) If they do not, consult user.

## STAGE 06: Integration with Assignment Framework
- Dual Purpose Architecture
- Extractable Components for Assignment Submission
  - task.py (from task_definition.py)
  - grader.py (from core/grader.py)
  - test_data.sql (from test_data.py)
  - README.md
- Extraction Strategy
- Critical Requirements (under 300 lines, no Flask dependencies)

 **Context Needed**: 
 - `build_plan/app-summary.md`
 - `build_plan/ref-code-execution-sandbox.md` (grader)
 - `build_plan/ref-test-data-generation.md` (test data)
 - `build_plan/ref-task-definition-module.md` (task definition)
