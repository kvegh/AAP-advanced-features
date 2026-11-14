# linux_updates

When selected by the entrypoint, register the RHEL 9 guest with the existing
protected RHSM organization/activation key, enable BaseOS/AppStream and update
installed packages. Reboot only after changed packages, then verify no updates
remain.

The entrypoint defaults `provisioning.update_packages` to true. Sniper patch
clients explicitly set false, which skips this entire role and preserves their
patchable image baseline. No Satellite registration is performed here.
