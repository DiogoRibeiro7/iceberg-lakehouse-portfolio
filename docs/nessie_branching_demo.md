# Nessie Branching Demo

This walkthrough demonstrates isolated development on a Nessie branch, validation, and promotion to `main`.

## Script

- `sql/nessie_branching_demo.sql`

## Workflow

1. List current references with `SHOW REFERENCES IN local`.
2. Create `dev` from `main`.
3. Switch to `dev` and apply table/data changes.
4. Validate data on `dev`.
5. Switch back to `main` and verify isolation.
6. Merge `dev` into `main`.
7. Validate promoted results on `main`.
8. Drop `dev` (optional cleanup).

## What to verify

- Before merge:
  - `main` does not contain in-progress changes from `dev`.
- After merge:
  - `main` contains the `dev` changes exactly as validated.

## Notes

- Keep naming explicit (`dev`, `main`) to avoid accidental writes.
- Treat each demo branch like a pull request workflow:
  - write in branch
  - validate in branch
  - merge to main
