
#!/usr/bin/env bash

set -euo pipefail

# Required environment variables:
# DEPLOY_HOST: remote SSH hostname or IP address
# DEPLOY_USER: SSH username
# DEPLOY_PATH: destination directory on the remote host

: "${DEPLOY_HOST:?ERROR: Set DEPLOY_HOST}"
: "${DEPLOY_USER:?ERROR: Set DEPLOY_USER}"
: "${DEPLOY_PATH:?ERROR: Set DEPLOY_PATH}"

# Validate values before constructing the command.
if [[ ! "$DEPLOY_HOST" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "ERROR: DEPLOY_HOST contains invalid characters." >&2
    exit 1
fi

if [[ ! "$DEPLOY_USER" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "ERROR: DEPLOY_USER contains invalid characters." >&2
    exit 1
fi

if [[ "$DEPLOY_PATH" != /* ]]; then
    echo "ERROR: DEPLOY_PATH must be an absolute path." >&2
    exit 1
fi

# Print the command only. Do not connect to the remote host.
printf 'Deployment command (not executed):\n'
printf 'ssh %q@%q %q\n' \
    "$DEPLOY_USER" \
    "$DEPLOY_HOST" \
    "cd '$DEPLOY_PATH' && ./deploy.sh"
