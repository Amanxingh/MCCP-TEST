# GridPulse Operations Runbook

## Purpose

GridPulse Outage Analytics is a command-line utility that helps energy operations teams review smart-meter outage events. It reports outage activity by feeder, affected customers, event history, recurring outages, and priority follow-up candidates.

Run it when reviewing outage activity, investigating repeated interruptions, validating database updates, or preparing an operational summary.

## Preconditions

Before running GridPulse, ensure the following are available:

- Python 3.12 recommended.
- Git Bash on Windows.
- The project repository is checked out on the intended working branch.
- The `src/`, `tests/`, `vendor/`, and `scripts/` directories are present.
- Vendored pytest wheels and their required dependencies are available for offline installation.
- Docker Desktop is running if container verification is required.

From the repository root, inspect the working tree:

```bash
git status
git branch --show-current
python verify_env.py
```

Create and activate a virtual environment, then install development dependencies offline:

```bash
python -m venv .venv
. .venv/Scripts/activate
python -m pip install --no-index --find-links=vendor -r requirements-dev.txt
```

No deployment environment variables are required for normal local reporting. If the deployment preparation script is used, set `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_PATH`. It should validate these values and print the proposed SSH command without connecting to a remote host.

## Normal operation

### 1. Initialize the database

From the repository root, initialize the local database using the CLI:

```bash
python -m gridpulse.cli init-db
```

If Python cannot locate the package, configure the source directory:

```bash
export PYTHONPATH=src
python -m gridpulse.cli init-db
```

Use the database path option supported by the CLI if a non-default database location is required. Initialization may create or reset local data, so verify the implementation's behavior before running it against any database that must be preserved.

### 2. Generate the report

```bash
python -m gridpulse.cli report
```

Review the report for feeder-level event counts, affected customers, recent meter events, and other supported summaries. Confirm that the output matches the deterministic seed data when using a freshly initialized development database.

Check the available options if needed:

```bash
python -m gridpulse.cli --help
```

### 3. Run tests

Run the full project check script:

```bash
bash scripts/run_checks.sh
```

The script should detect an available Python interpreter, perform its environment check, execute pytest, and write a text summary. Review both the terminal output and the generated summary.

### 4. Prepare a submission archive

```bash
bash scripts/package_submission.sh
```

The required output is:

`submission/gridpulse-submission.tar.gz`

Confirm that the script excludes Git metadata, virtual environments, caches, generated databases, and previous submission archives.

## Container operation

### Live Docker verification

If Docker Desktop is available, build the image from the repository root:

```bash
docker build -f docker/Dockerfile -t gridpulse-tests .
```

Run the container's default test command:

```bash
docker run --rm gridpulse-tests
```

Validate the Compose configuration:

```bash
docker compose -f docker/docker-compose.yml config
```

Start the service:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Stop the service when verification is complete:

```bash
docker compose -f docker/docker-compose.yml down
```

The Compose configuration is intended to use a named data volume and an isolated bridge network. Confirm the configured database path and CLI command before relying on persistent data.

### Static-review limitation

If Docker is unavailable, do not claim that the image was built or executed. Review `docker/Dockerfile`, `docker/docker-compose.yml`, and `docker/STATIC_REVIEW.md` against the required image, build context, offline dependency installation, volume, network, command, and image-tag conventions. Record that container execution was not performed.

## Verification

A successful verification requires the environment check and the complete pytest suite to pass.

Expected checks include:

- The environment check identifies a usable Python interpreter.
- Pytest completes with no failed tests.
- Database queries use columns that exist in the initialized SQLite schema.
- The CLI produces the expected report from the deterministic seed data.
- Docker checks pass when Docker is available, or static review is documented when it is not.
- The submission archive can be listed and extracted successfully.

Inspect the output and generated check summary after running:

```bash
bash scripts/run_checks.sh
```

To run tests directly with more detail:

```bash
python -m pytest -v
```

For additional diagnostic information, inspect application logs and any error messages emitted by the CLI. If the application writes logs to a file, use the configured log path; otherwise, inspect the terminal output.

A SQLite error such as `no such column` indicates that a query and the actual database schema may not agree. Compare the relevant query in `src/gridpulse/repository.py` with the schema and initialization code in `src/gridpulse/db.py`. Rerun initialization only after confirming that doing so will not destroy data that must be retained.

## Rollback / recovery

### 1. Inspect the working tree

```bash
git status
git diff
git diff --cached
```

Review all changes before discarding anything.

### 2. Restore tracked files

To discard uncommitted changes to a specific tracked file:

```bash
git restore path/to/file
```

To unstage a file without discarding its changes:

```bash
git restore --staged path/to/file
```

Avoid `git reset --hard` unless you intentionally want to discard all uncommitted tracked changes. Back up any work that must be preserved first.

### 3. Remove generated data

Identify the actual database path before deleting generated files. If the database is disposable development data, stop any running application that uses it, then remove only that specific generated database.

For example, if the confirmed generated database is `data/gridpulse.db`:

```bash
rm -f data/gridpulse.db
```

Do not remove a database that contains data you need to keep. A named Docker volume may retain data after containers stop; inspect the volume before removing it. Avoid `docker compose down -v` unless deleting the Compose-managed volume is intentional.

### 4. Rerun verification

After recovery, rerun:

```bash
python verify_env.py
bash scripts/run_checks.sh
```

If tests pass, review and commit the intended changes. Push the working branch to `origin` using its configured branch name.

### 5. Verify the submission archive

List the archive contents:

```bash
tar -tzf submission/gridpulse-submission.tar.gz
```

Extract it into a temporary directory to check that it is valid:

```bash
mkdir -p submission/verify
tar -xzf submission/gridpulse-submission.tar.gz -C submission/verify
```

Inspect the extracted structure. Remove the temporary directory afterward:

```bash
rm -rf submission/verify
```

Recreate the archive after making final changes, then repeat the listing and extraction checks before submission.