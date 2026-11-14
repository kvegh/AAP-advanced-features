#!/bin/sh
# Offline clone identity/access operations: ../README.md#supporting-tools
set -eu

rm -f /etc/ssh/ssh_host_*
truncate -s 0 /etc/machine-id
mkdir -p /var/lib/dbus
rm -f /var/lib/dbus/machine-id
ln -s /etc/machine-id /var/lib/dbus/machine-id
