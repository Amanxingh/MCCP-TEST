
#!/usr/bin/env bash

set -u

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUMMARY_FILE="$PROJECT_ROOT/checks_summary.txt"
TEST_OUTPUT="$PROJECT_ROOT/.checks_test_output.txt"

cd "$PROJECT_ROOT" || exit 1

# Detect an available Python command.
if command -v python3 >/dev/null 2>&1; then
    PYTHON=(python3)
elif command -v python >/dev/null 2>&1; then
    PYTHON=(python)
elif command -v py >/dev/null 2>&1; then
    PYTHON=(py -3)
else
    echo "ERROR: Python was not found." | tee "$SUMMARY_FILE"
    exit 1
fi

{
    echo "GridPulse Check Summary"
    echo "======================="
    printf 'Python command:'
    printf ' %s' "${PYTHON[@]}"
    echo
    echo
} > "$SUMMARY_FILE"

# Check Python environment.
if "${PYTHON[@]}" --version >> "$SUMMARY_FILE" 2>&1; then
    echo "Environment check: PASS" | tee -a "$SUMMARY_FILE"
else
    echo "Environment check: FAIL" | tee -a "$SUMMARY_FILE"
    exit 1
fi

# Run the test suite and save its output.
if "${PYTHON[@]}" -m pytest -v > "$TEST_OUTPUT" 2>&1; then
    cat "$TEST_OUTPUT"
    echo "Tests: PASS" | tee -a "$SUMMARY_FILE"
else
    cat "$TEST_OUTPUT"
    echo "Tests: FAIL" | tee -a "$SUMMARY_FILE"
    cat "$TEST_OUTPUT" >> "$SUMMARY_FILE"
    rm -f "$TEST_OUTPUT"
    exit 1
fi

rm -f "$TEST_OUTPUT"
echo "Summary saved to: $SUMMARY_FILE"
exit 0
