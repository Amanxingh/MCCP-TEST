# GridPulse Outage Analytics

GridPulse is a small internal utility used by an energy operations team to review smart-meter outage events. The repository is a brownfield starter: the project structure, deterministic SQLite seed data, tests, and documentation skeletons are present, but several implementation details are intentionally incomplete.

The application uses only the Python standard library at runtime. Pytest wheels are vendored in `vendor/` so the local test setup can run without downloading packages.

## Business scenario

A regional utility needs a reliable command-line report that answers these questions:

- Which feeders have the most outage events and affected customers?
- Which meter has the latest event, and is that event still active?
- Which meters have recurring outages?
- Which active or historical events should receive priority follow-up?
- Can the same checks be repeated locally, in a container, and in a CI pipeline?

## Current project layout

```text
src/gridpulse/       Application package
tests/               Pytest suite with deterministic expected values
scripts/             Bash helper scripts for checks, packaging, and remote-command preparation
docker/              Dockerfile, Compose file, and static review path
docs/                Candidate documentation templates
data/                Generated SQLite database location
vendor/              Offline pytest wheels
verify_env.py        Local environment self-check
```

## Getting started

Use Git Bash on Windows.

```bash
./verify_env.py
# or, if the file is not executable in your checkout:
python verify_env.py
```

If pytest is not already installed, create a local virtual environment and install from the vendored wheels:

```bash
python -m venv .venv
. .venv/Scripts/activate
python -m pip install --no-index --find-links=vendor -r requirements-dev.txt
```

Run the checks:

```bash
./scripts/run_checks.sh
```

The baseline tests are expected to fail until the TODO items are implemented.

## Working tasks

See `TASKS.md` for the complete task list. Keep commits small and meaningful. Use the existing `origin` remote supplied with the kit; it is a local bare repository and requires no network access.

## Submission

When finished, commit your work, push your working branch to `origin`, and create `submission/gridpulse-submission.tar.gz` using `scripts/package_submission.sh`. The archive must exclude `.git`, `.venv`, caches, generated databases, and prior submission archives.

## Documentation to complete

- `README.md`: finish setup, usage, and troubleshooting notes.
- `RUNBOOK.md`: write operational steps another engineer can follow.
- `docs/PR_SUMMARY.md`: summarize the branch as if it were under review.
- `docs/STAKEHOLDER_UPDATE.md`: write a concise non-technical status update.
