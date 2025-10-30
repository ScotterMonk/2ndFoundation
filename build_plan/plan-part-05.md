## Application Pages & Flow

### Navigation Menu

```
┌─────────────────────────────────────────────────────────┐
│  🔮 2nd Foundation                                      │
│  ───────────────────────────────────────────────────────│
│  [Home] [Search] [Upload] [RL Task] [Testing] [Admin]  │
└─────────────────────────────────────────────────────────┘
```

### Page Descriptions

#### 1. Home (`/`)
- Project overview and purpose
- Quick stats: documents indexed, searches performed, model submissions
- Quick search bar
- Recent activity feed

#### 2. Search (`/search`)
- Main search interface using production hybrid search
- Real-time results display
- Relevance scores shown
- Click to view full document
- Query history sidebar

#### 3. Upload (`/upload`)
- Drag-and-drop document upload
- Supported formats: PDF, TXT, MD, DOCX
- Batch processing progress
- Upload history with status

#### 4. RL Task (`/rl-task/*`) - **Core Assignment Interface**

**a) Overview (`/rl-task`)**
- Complete task description (what models receive)
- RRF algorithm explanation
- Expected function signature
- Example test cases
- Download starter template

**b) Submit (`/rl-task/submit`)**
- Code editor (Monaco or textarea)
- File upload option for `search.py`
- "Run Grader" button
- Real-time execution feedback

**c) Results (`/rl-task/results/<submission_id>`)**
- Overall pass/fail status
- Score breakdown by test category
- Per-test-case details:
  - Expected vs actual documents
  - Ranking comparison
  - Error messages
- Performance metrics
- Code diff viewer (vs reference implementation)
- "Submit Again" button

**d) History (`/rl-task/history`)**
- Table of all model submissions
- Columns: Model, Score, Time, Status
- Score progression chart
- Filter by model type

#### 5. Testing (`/testing`)
- Run full test suite manually
- Individual test case explorer
- Performance benchmarks
- Coverage reports
- Compare reference impl vs model attempts

#### 6. Admin (`/admin`)
- Document management (view, edit, delete)
- Database statistics
- Re-index documents
- Clear embeddings cache
- Export test data
