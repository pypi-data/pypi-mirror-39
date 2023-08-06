#!/usr/bin/env bash
#
# liblightnvm
#
# - Choose device identifier based on NVM_CLI_BE_ID
# - Optionally configure SPDK hugemem
#
# Set NVM device identifier
export NVM_DEV_IDENT
if [[ "$NVM_CLI_BE_ID" == "4" ]]; then
  NVM_DEV_IDENT="traddr:$PCI_DEV_NAME"
else
  NVM_DEV_IDENT="/dev/$NVME_DEV_NAME"
fi
#
# OPTIONAL: Change the memory assigned to SPDK
#export HUGEMEM=8192
#
