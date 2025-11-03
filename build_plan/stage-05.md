# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

The following is one stage in a multi-stage "application creation project". Do not stray into doing more than is set out here. If you have ideas that might involve additions:
1) Look at the other stages (`build_plan/stage-**.md`) to be sure they do not already cover the functionality.
2) If they do not, consult user.

## STAGE 05: BUILD RL TASK COMPONENTS
- Deep dive into RL task now that infrastructure exists.

### Phase 1: Understand the RL Task Flow (Use `build_plan/app-summary.md`)
- The Actual Workflow
- The RL Task: Hybrid Search with RRF
  - What the Model Receives (Task Prompt)
  - Verification Approach
  - Expected Model Failure Modes
  - Grading Criteria

**Context to use:**
- `build_plan/ref-search-functions.md` (search functions)
- (does not exist yet) `app/rl_task/task_definition.py` (extracted to `task.py` for assignment)
- `build_plan/ref-task-definition-module.md` (task definition module)

### Phase 2: Code Execution Sandbox (for Grading)
Build Security-critical grading logic after understanding the task.
- Security Requirements
- AST Parsing for Malicious Code Detection
- Timeout Enforcement
- Restricted Globals
- execute_model_code function implementation

Use `build_plan/ref-code-execution-sandbox.md` (grader)

Additional references:
- `build_plan/ref-embeddings.md` - For app/core/embeddings.py implementation (generate_embedding function used by search and test data)
- `build_plan/ref-upload-processing.md` - For app/core/upload.py document processing logic

