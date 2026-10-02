# Candidate Task List

Complete the work in the repository directly. You may use AI tools, but you remain responsible for every command and line of code you submit. Be prepared to explain your choices in the technical interview.

## 1. Environment and repository setup

1. Run `verify_env.py` and resolve any required-tool findings.
2. Configure a repository-local Git author name and email. Do not change global Git settings.
3. Confirm that `origin` points to the supplied local bare remote.
4. Create and switch to a working branch named `candidate/l1-solution`.
5. Fetch the supplied `feature/outage-priority-wip` branch, merge it into your working branch, and resolve the resulting conflict safely.
6. Keep the repository clean with appropriate `.gitignore` rules and clear commits.

## 2. SQLite schema, seed data, and queries

Complete the TODO items in `src/gridpulse/db.py` and `src/gridpulse/repository.py`:

- Create a relational schema with keys, constraints, and useful indexes.
- Load the deterministic seed data without duplicating rows when rerun.
- Implement joins, aggregation, a window function, and a CTE.
- Add an index and provide an `EXPLAIN QUERY PLAN` helper for the latest-event lookup.

## 3. Python implementation and tests

Complete the TODO items in `src/gridpulse/models.py`, `service.py`, `logging_utils.py`, `reporting.py`, and `cli.py`:

- Implement the outage duration and priority model.
- Use clear exceptions and structured logging.
- Implement the decorator, generator, context manager, regex validation, and functional helpers requested by the tests.
- Replace `tests/test_candidate_pytest.py` with two meaningful tests of your own.
- Make the provided test suite pass without changing baked-in expected values.

## 4. CLI and shell workflows

Complete the TODO items in `scripts/`:

- `run_checks.sh` must auto-detect `python3`, `python`, or `py -3`, run the environment check and tests, and write a text summary using standard CLI tools.
- `package_submission.sh` must create a compressed tar archive suitable for Windows bsdtar or Git Bash.
- `remote_deploy.sh` must validate required environment variables and print the SSH command it would run. It must not connect to a remote host.
- Do not rely on executable permission bits alone; document how to run each script with `bash` on Windows.

## 5. Container path

Complete `docker/Dockerfile` and `docker/docker-compose.yml`.

If Docker Desktop is available, build and run the checks in a container and tag the image using the convention in `docker/STATIC_REVIEW.md`. If Docker is unavailable, complete the static review instead. The two paths are designed to demonstrate the same container concepts.

## 6. CI/CD workflow

Complete `.github/workflows/ci.yml`:

- Run tests on pushes and pull requests.
- Install pytest from `vendor/` without downloading test dependencies.
- Fail the job when tests fail.
- Add a manual production-promotion stage that uses an environment and secrets safely.

## 7. Documentation and submission

1. Finish all documentation templates listed in `README.md`.
2. Run the full check script.
3. Commit and push your working branch.
4. Create the submission archive and verify that it extracts cleanly.
5. Be ready to walk through your implementation, trade-offs, and verification steps.
