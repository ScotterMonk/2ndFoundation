# 251022_media_pipeline — user query
Short plan name: 251022_media_pipeline
Project size/complexity: Multi-Phase (larger project), many tasks per phase
Autonomy level: High (rare direction)
Testing type: Use browser

Goal: Make a detailed plan to simplify (remove unnecessary complexity) one part of this application as shown below.
Complexity/simplification: use the rules in @/.roo/docs/simplification.md
CRITICAL to Keep in mind:
- IMDB is used in this application.
- TVDB and TMDB are not currently in use but may be used later.

Cascade: Media File Operations
Current State: 21 duplicate functions across utils/media.py and utils/media_core.py
- validate_file, allowed_file (2 implementations each)
- generate_unique_filename, get_file_hash, get_file_size_mb (2 each)
- process_uploaded_files, save_uploaded_file, delete_media_files (2 each)
- generate_thumbnail, create_upload_directories, get_media_metadata (2 each)

Insight: "All file operations are: validate → transform → store/retrieve"

Proposed Solution: Single MediaFileHandler with pipeline pattern
- Validation pipeline (type, size, hash)
- Transform pipeline (thumbnail, metadata)
- Storage pipeline (unique naming, directories)

Cascade Eliminates:
- 21 duplicate function implementations
- Multiple validation approaches
- Inconsistent error handling

Files Affected:
- utils/media.py
- utils/media_core.py
- routes/utils_admin_media.py
- routes/utils_user_media.py