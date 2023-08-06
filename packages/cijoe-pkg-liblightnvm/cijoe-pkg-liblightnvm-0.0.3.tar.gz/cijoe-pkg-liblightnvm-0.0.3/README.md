# cijoe-pkg-liblightnvm - Collection of test cases suites and plans

## Installation

Install:

```bash
pip install cijoe-pkg-liblightnvm
```

## Create environment definition for CIJOE

Run CIJOE interactively and define the target environment:

```bash
# Start cijoe
cijoe

# Use refence definitions as a template for defining your environment
cat $CIJ_ENVS/refenv-u1604.sh > target_env.sh
tail -n +2 $CIJ_ENVS/refenv-liblightnvm.sh >> target_env.sh

# Open up your favorite editor and modify accordingly
vim target_env.sh
```

## Create virtual environment definition for CIJOE

Run CIJOE interactively and define the target environment:

```bash
# Start cijoe
cijoe

# Use refence definitions as a template for defining your environment
cat $CIJ_ENVS/refenv-u1604.sh > target_env.sh
tail -n +2 $CIJ_ENVS/qemu.sh >> target_env.sh
tail -n +2 $CIJ_ENVS/refenv-liblightnvm.sh >> target_env.sh

# Open up your favorite editor and modify accordingly
vim target_env.sh
```

## Running tests

Start the test-runner and view the report:

```bash
# Create directory to store results
RESULTS=$(mktemp -d trun.XXXXXX -p /tmp)

# Run using the testplan for Open-Channel 2.0 devices
cij_runner \
    $CIJ_TESTPLANS/OCSSD_S20_IOCTL.plan \
    target_env.sh \
    --output $RESULTS

# Create test report
cij_reporter $RESULTS

# Inspect the test-report
xdg-open $RESULTS/report.html
```
