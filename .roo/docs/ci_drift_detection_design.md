# CI Drift Detection Design
Objective: To automatically detect and report on any drift between the live database, the ORM models, and the canonical schema documentation.

## Trigger
- On every push to the `main` branch
- Nightly schedule (eg, 02:00 UTC)

## Workflow Steps
1) Setup: Install dependencies and configure database connection.
- Check out repository
- Install Python (3.10+)
- Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```
- Provide DB credentials via CI secrets as environment variables (consumed by the app the same way as `@\.env`):
    - PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
- Ensure working directory: repository root

2) Run database-vs-models comparison.
```powershell
python utils/schema_inspector.py compare-db-models
```

3) Validate docs match the database.
```powershell
python utils/schema_inspector.py validate
```

4) Evaluate results and enforce policy.
- If either command returns a non-zero exit code, mark the job as failed
- Optionally collect and upload any generated reports from `@\.roo\docs\schema_reports`

5) Notify on failure.
- Fail the CI job
- Post a notification (eg, Slack webhook) and/or comment on the pull request summarizing discrepancies and next steps

## Future Enhancements
- Automatically create a GitHub issue when drift is detected (include output artifacts)
- Attach diffs of affected model files and documentation sections to CI logs
- Provide a diagnostics mode that also runs:
    ```powershell
    python utils/schema_inspector.py introspect
    ```
  and archives outputs for review
- Gate merges to `main` when drift is present unless an override label (eg, `schema-override-approved`) is applied
- Add a local pre-commit hook for a lightweight models-vs-docs check