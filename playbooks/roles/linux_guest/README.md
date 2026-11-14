# linux_guest

Verify authenticated Linux access, exact requested configured hostname/vCPU allocation,
memory including kernel crash reservation, root filesystem. Both image modes preserve application/installer content.
Upstream images do not need an inherited AAP service account.

Inputs are the protected `provisioning` dictionary and provisioned-host metadata
from `linux_vm`. This role gathers guest facts and performs read-only checks.
It does not install software or register to Satellite.
