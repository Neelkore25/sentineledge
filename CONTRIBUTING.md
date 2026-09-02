# Contributing to SentinelEdge

Thank you for contributing to SentinelEdge!

## Development Setup
1. **Backend**:
   ```bash
   cd apps/api
   pip install -r requirements.txt
   python -m pytest tests -v
   python main.py
   ```
2. **Frontend**:
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

## Branch Naming Convention
- `feature/<name>` — New capabilities or components
- `fix/<name>` — Bug fixes and engine adjustments
- `docs/<name>` — Research and documentation updates

## Pull Request Guidelines
- Ensure all backend unit and API tests pass: `pytest apps/api/tests`
- Ensure frontend passes typechecking: `npm run typecheck`
- Keep commits atomic and clearly described.
