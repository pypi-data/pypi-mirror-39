import os
import platform

UBUNTU_UPSTART_JOB_FILE = \
"""# {tty} - getty
#
# This service maintains a getty on {tty} from the point the system is
# started until it is shut down again.

start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]

respawn
exec /sbin/getty -8 38400 -n -i -l {path} {tty}
"""

UBUNTU_SYSTEMD_JOB_FILE = \
"""
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

[Unit]
Description=Getty on %I
Documentation=man:agetty(8) man:systemd-getty-generator(8)
Documentation=http://0pointer.de/blog/projects/serial-console.html
After=systemd-user-sessions.service plymouth-quit-wait.service getty-pre.target
After=rc-local.service

# If additional gettys are spawned during boot then we should make
# sure that this is synchronized before getty.target, even though
# getty.target didn't actually pull it in.
Before=getty.target
IgnoreOnIsolate=yes

# IgnoreOnIsolate causes issues with sulogin, if someone isolates
# rescue.target or starts rescue.service from multi-user.target or
# graphical.target.
Conflicts=rescue.service
Before=rescue.service

# On systems without virtual consoles, don't start any getty. Note
# that serial gettys are covered by serial-getty@.service, not this
# unit.
ConditionPathExists=/dev/tty0

[Service]
# the VT is cleared by TTYVTDisallocate
# The '-o' option value tells agetty to replace 'login' arguments with an
# option to preserve environment (-p), followed by '--' for safety, and then
# the entered username.
ExecStart=-/sbin/agetty -8 38400 -n -i -l {path} {tty}
Type=idle
Restart=always
RestartSec=0
UtmpIdentifier=%I
TTYPath=/dev/%I
TTYReset=yes
TTYVHangup=yes
TTYVTDisallocate=yes
KillMode=process
IgnoreSIGPIPE=no
SendSIGHUP=yes

# Unset locale for the console getty since the console has problems
# displaying some internationalized messages.
UnsetEnvironment=LANG LANGUAGE LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION

[Install]
WantedBy=getty.target
DefaultInstance=tty1
"""


def install(tty_dev, greeter_path):
    dist, version, nick = platform.dist()
    if dist == 'Ubuntu':
        major, minor = (int(i) for i in version.split('.'))
        if 10 <= major < 18:
            install_on_ubuntu_14(tty_dev, greeter_path)
            return
        elif major >= 18:
            install_on_ubuntu_18(tty_dev, greeter_path)
            return
    raise NotImplementedError("{} {} not supported".format(dist, version))


def move_to_backup(path):
    backup_path = path + ".before_greeter"
    if not os.path.exists(backup_path):
        os.rename(path, backup_path)


def install_on_ubuntu_14(tty_dev, greeter_path):
    template = UBUNTU_UPSTART_JOB_FILE.format(tty=tty_dev, path=greeter_path)
    job_path = "/etc/init/{tty_dev}.conf".format(tty_dev=tty_dev)
    move_to_backup(job_path)
    with open(job_path, "w") as f:
        f.write(template)

def install_on_ubuntu_18(tty_dev, greeter_path):
    template = UBUNTU_SYSTEMD_JOB_FILE.format(tty=tty_dev, path=greeter_path)
    job_path = "/etc/systemd/system/getty@{tty_dev}.service".format(tty_dev=tty_dev)
    with open(job_path, "w") as f:
        f.write(template)
