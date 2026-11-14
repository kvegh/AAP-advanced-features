# linux_root_growth

Grow only the existing last GPT root partition and its XFS filesystem. Preserve
the root partition's start, type, UUID and neighboring partitions; reject other
layouts. The idempotent helper validates live storage and retains a private
partition-table backup before changing the last partition's end.

## Supporting tools

The existing small `files/grow-root.py` helper coordinates sfdisk, lsblk, findmnt
and xfs_growfs because the current generic creator requires exact GPT identity
preservation and a single validated root-growth operation. This relocation adds
no package or module installation. Focused storage fixtures test supported and
rejected layouts; final relocated AAP runtime verification remains separate.

The guest must already supply those native tools. The Ansible task installs the
helper under its generic runtime filename and reports its actual change result.
