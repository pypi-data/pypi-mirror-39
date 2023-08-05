# cijoe-pkg-liblightnvm - Collection of test cases suites and plans

## Installation

```bash
# Install from PyPi via pip
pip install cijoe-pkg-liblightnvm
```

## Usage

Run CIJOE interactively and define the target environment:

```
# Start cijoe
cijoe

# Copy refenv-definition to use as template, modify according to you environment
cat $CIJ_ENVS/refenv-u1604.sh > target_env.sh
cat $CIJ_ENVS/refenv-liblightnvm >> target_env.sh
vim target_env.sh
```

Start the test-runner and view the report:

```bash
# Create directory to store results
RESULTS=$(mktemp -d trun.XXXXXX -p /tmp)

# Run using the testplan for Open-Channel 2.0 devices
cij_runner \
    $CIJ_TESTPLANS/OCSSD_S20.plan \
    $CIJ_ENVS/target_env.sh
    --output $RESULTS

# Create test report
cij_reporter $RESULTS

# Inspect the test-report
xdg-open $RESULTS/report.html
```
