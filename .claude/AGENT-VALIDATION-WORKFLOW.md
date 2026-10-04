# Agent Validation Workflow for Morning Prompt

This documents where agents are integrated into the development workflow to validate changes before considering them complete.

## Workflow Steps (with Agent Checkpoints)

### 1. Code Changes
- Modify `editor.py`, `newsletter-final.html`, or supporting files
- Update data structures and logic

### 2. **AGENT CHECKPOINT: Code Review Agent** ✓
```
Spawn: Agent for code review
Validates:
- Python syntax and logic correctness
- HTML/JavaScript functionality
- Data transformation integrity
- Edge cases and error handling
```

### 3. Generate/Build Output
- Run `editor.py` to generate newsletter
- Process data through template system
- Output to `output/newsletter-final.html`

### 4. **AGENT CHECKPOINT: QA Validation Agent** ← Currently Here
```
Spawn: QA Agent for production validation
Validates:
- Newsletter renders correctly (no wireframe/empty)
- All 5 stories display with full content
- Word of Day rotation working (no repeats)
- Vote counts from Supabase (not hardcoded)
- UI interactive (buttons work, console clean)
- No fake/demo data exposed
```

### 5. Data Persistence
- Save stories to Supabase database
- Update `published.json` for deduplication
- Track `words_of_day.json` usage

### 6. **AGENT CHECKPOINT: Data Integrity Agent** (Planned)
```
Spawn: Agent to verify database state
Validates:
- Stories saved correctly to Supabase
- Vote counts queryable
- No duplicate stories
- Word rotation state persisted
```

### 7. Deployment Ready
- Commit to Git (when validated)
- Push to GitHub (when ready)
- Deploy to Vercel (when approved)

---

## Where Each Agent Fits

| Phase | Agent Type | Purpose | Output |
|-------|-----------|---------|--------|
| After code edits | Code Review | Syntax, logic, correctness | Pass/fail on code quality |
| After build | QA Validation | UI/UX, content display, real data | Pass/fail on user experience |
| After persistence | Data Integrity | Database, records, deduplication | Pass/fail on data layer |
| Before deploy | Integration Test | End-to-end workflow | Pass/fail on production readiness |

---

## Recent Session: Oct 4, 2026

### Changes Made (Fixed Data Sources)
- Removed hardcoded fake vote counts (342/28, etc.)
- Implemented Word of Day rotation system
- Added real Supabase vote fetching
- Fixed newsletter template injection

### Agents Spawned
- **QA Agent (a6dad84f9c630602f)**: Validating newsletter rendering and data sources
  - Status: Running
  - Expected validation: Content display, Word of Day, vote system

### Next Agents to Spawn
1. **Data Integrity Agent**: Verify Supabase state after generation
2. **Integration Test Agent**: Full end-to-end workflow test

---

## Agent Validation Checklist

Every change should trigger this sequence:
- [ ] Code changes made
- [ ] Agent: Code review spawned ← *(was missing, adding now)*
- [ ] Build executed
- [ ] Agent: QA validation spawned ← *(just done)*
- [ ] Data persistence
- [ ] Agent: Data integrity spawned ← *(next)*
- [ ] All agents pass
- [ ] Commit to Git
- [ ] Ready for deployment


## Environment Setup

### Python Execution
**Required**: Anaconda Python (user's machine uses Anaconda)
**Path**: `C:\Users\jaina\anaconda3\python.exe`
**Command Pattern**: `& "C:\Users\jaina\anaconda3\python.exe" editor.py`

**DO NOT use**:
- System Python
- Virtual environments
- Any path other than Anaconda installation

### Artifact Generation
**Blocked**: Do not generate any artifacts in this project
- No .html files as artifacts
- No markdown pages
- Only file-based output to `/output` directory

### Command Execution
- Use PowerShell for Windows commands
- Use Bash for Git commands
- Always specify full Anaconda path for Python execution

