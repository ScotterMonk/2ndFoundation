# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

## STAGE 07: BUILD TESTS
- Unit Tests (app/tests/test_search.py)
  - test_vector_search
  - test_keyword_search
  - test_hybrid_search_basic
  - test_hybrid_search_empty_query
  - Use `build_plan/ref-unit-tests.md`
- Integration Tests (app/tests/test_grader.py)
  - test_grade_correct_submission
  - test_grade_incorrect_k_value
  - Use `build_plan/ref-integration-tests.md`

**Context Needed**:
- `build_plan/ref-search-functions.md` (search functions)
- `build_plan/ref-code-execution-sandbox.md` (grader)