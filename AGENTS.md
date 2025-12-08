# Agent instructions

- Repository-wide: include a brief summary of changes and a list of tests executed in final responses, and cite files or commands referenced.
- Backend changes (within `api/`): run `python -m compileall api` before committing to ensure syntax validation.
- Frontend changes (within `iris-frontend/`): prefer running `npm test` when modifying React code; if not run, mention why in the summary.
