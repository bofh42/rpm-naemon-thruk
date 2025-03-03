#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2025-present Peter Tuschy (foss@bofh42.de)

# bash version 4 or later
[ ${BASH_VERSION%%.*} -ge 4 ] || exit 1

export LANG=en_US.UTF-8

need_cmd() { hash "$1" 2>/dev/null; if [ $? -ne 0 ]; then echo "ERROR: script ${0##*/} needs command $1"; exit 1; fi; }
for i in readlink dnf egrep awk sed rpm2cpio cpio ; do need_cmd $i ; done

SCRIPT=$(readlink -f $0)
WHERE=${SCRIPT%/*}

cd "${WHERE}" || exit $?

if [[ $1 =~ --cleanup ]]; then
  CLEANUP=1
  shift
fi

REPO="https://download.opensuse.org/repositories/home:/naemon/AlmaLinux_9/"
RPMs="$(dnf list --disablerepo=* --repofrompath=naemon-el9-obs,${REPO} | grep -E 'naemon-el9-obs\s+$' | awk '{ print $1 }' | grep -E '\.src$' | sed -e 's|\.src$||g')"

for i in ${RPMs} ; do
  dnf download --source --disablerepo=* --repofrompath=naemon-el9-obs,${REPO} ${i} || break
  rpm2cpio ${i}-[[:digit:]]*.src.rpm | cpio --no-preserve-owner -miv '*.spec' || break && ( [ -n "${CLEANUP}" ] && rm ${i}-[[:digit:]]*.src.rpm )
done
