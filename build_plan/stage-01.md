# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

The following is one stage in a multi-stage "application creation project". Do not stray into doing more than is set out here. If you have ideas that might involve additions:
1) Look at the other stages (`build_plan/stage-**.md`) to be sure they do not already cover the functionality.
2) If they do not, consult user.

## STAGE 01: Modify Database Schema and Create Models
Scrutinize this for accuracy and completeness: 
- `build_plan/ref-database-schema.md` (db schema to build)

Goals:

Ignore the following tables that exist already in the database (files, languages, media, media_genres, media_types, notifications, system_settings, users_sessions, users_types). Do not change them or make models for them.

Add the table defs below (documents, search_queries, model_submissions, test_cases) as tables with columns to the database.

Modify the User model below based on structure of "users" table in the database.

Models (create in `models/` folder):
- Document Model (with embeddings and ts_vector)
- SearchQuery Model (analytics)
- ModelSubmission Model (RL task tracking)
- TestCase Model (grading test cases)
- User Model (authentication)
 
