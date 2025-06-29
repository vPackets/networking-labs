# 🖥️ Detailed Breakdown of SONiC System Output on a Cisco 8101-32H-O Switch

## 📦 System Login and Environment

```
Debian GNU/Linux 12 \n \l
admin@198.18.128.6's password:
Linux 8101-32H-O-1 6.1.0-22-2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.94-1 (2024-06-21) x86_64
```

- **Debian Version**: This system is running Debian GNU/Linux 12 (bookworm), with kernel 6.1.0-22-2-amd64.
- **PREEMPT\_DYNAMIC**: Indicates dynamic preemption is used, optimizing between latency and throughput.
- **x86\_64**: Confirms this is a 64-bit system.

---

## 🚪 Login Banner and MOTD

```
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --
Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.
Help:    https://sonic-net.github.io/SONiC/
```

- **SONiC Branding**: ASCII art and link to SONiC's documentation.
- **Security Warning**: Explicit note about monitoring and unauthorized access.

---

## 🧠 OS and Version Details

### `show version`

```
SONiC Software Version: SONiC.HEAD.1.2.0-7995b757b
SONiC OS Version: 12
Distribution: Debian 12.9
Kernel: 6.1.0-22-2-amd64
Build commit: 7995b757b
Build date: Sun Feb  9 04:30:37 UTC 2025
Built by: sonicci@sonic-ci-17-lnx.cisco.com

Platform: x86_64-8101_32h_o-r0
HwSKU: 32x100Gb
ASIC: cisco-8000
ASIC Count: 1
Serial Number: FLM25200A4B
Model Number: 8101-32H-O
Hardware Revision: 0.23
Uptime: 62 days
Load Average: 1.49, 1.13, 1.10
Date: Mon 16 Jun 2025 16:18:02
```

- **SONiC Version**: HEAD.1.2.0 (latest dev build, from Cisco CI).
- **Platform**: x86\_64 architecture, specific for Cisco 8101-32H-O switch.
- **SKU & ASIC**: 32x100Gb interfaces powered by Cisco-8000 ASIC.
- **Uptime**: Over 2 months, showing system reliability.
- **Build Metadata**: Includes builder ID, kernel details, and date.

---

## 🐳 Docker Containers in SONiC

Each SONiC service runs inside its own container. Here's a summary of the critical ones:

| Container Name              | Function                           | Size    |
| --------------------------- | ---------------------------------- | ------- |
| docker-syncd-cisco          | SAI implementation (Cisco)         | 1.11 GB |
| docker-database             | Redis-based config/state DB        | 339 MB  |
| docker-fpm-frr              | FRRouting - dynamic routing daemon | 391 MB  |
| docker-lldp                 | LLDP (Neighbor discovery)          | 377 MB  |
| docker-snmp                 | SNMP agent                         | 375 MB  |
| docker-orchagent            | Orchestration agent                | 372 MB  |
| docker-mux                  | MUX support for dual ToR           | 383 MB  |
| docker-sflow                | sFlow exporter                     | 360 MB  |
| docker-sonic-gnmi           | gNMI telemetry support             | 415 MB  |
| docker-platform-monitor     | Platform hardware monitoring       | 460 MB  |
| docker-sonic-mgmt-framework | Management REST/gNMI API stack     | 418 MB  |
| docker-eventd               | Event daemon for logging           | 331 MB  |
| docker-router-advertiser    | Router advertisement service       | 331 MB  |
| docker-dhcp-relay           | DHCP relay agent                   | 340 MB  |
| docker-macsec               | MACSec encryption support          | 362 MB  |
| docker-ipxeserver-cisco     | PXE server implementation          | 353 MB  |
| docker-teamd                | Link Aggregation (LAG) daemon      | 359 MB  |

---

## 🧰 Platform Hardware Info

### `show platform summary`

```
Platform: x86_64-8101_32h_o-r0
HwSKU: 32x100Gb
ASIC: cisco-8000
ASIC Count: 1
Serial Number: FLM25200A4B
Model Number: 8101-32H-O
Hardware Revision: 0.23
```

- **HwSKU**: Maps to supported port configuration and feature set.
- **ASIC**: Cisco-8000, indicating proprietary Cisco silicon.
- **Revision**: 0.23 shows maturity level of hardware version.

---

## 💾 Configuration Save

### `sudo config save -y`

```
Running command: /usr/local/bin/sonic-cfggen -d --print-data > /etc/sonic/config_db.json
```

- **Purpose**: Saves the in-memory configuration DB to disk (JSON).
- **Tool**: `sonic-cfggen` serializes database to persistent file.
- **Location**: `/etc/sonic/config_db.json`

---

## ✅ Image Installation

### `sudo sonic-installer install http://...bin`

```bash
admin@8101-32H-O-1:~$ sudo sonic-installer install http://198.18.140.3:8080/sonic-cisco-8000.bin
New image will be installed, continue? [y/N]: y
Downloading image...
...98%, 1709 MB, 109408 KB/s, 0 seconds left...
efi not supported - exiting without verification

Installing image SONiC-OS-202405.1.3.0z and setting it as default...
Command: bash /tmp/sonic_image
chown: warning: '.' should be ':': ‘root.root’
Verifying image checksum ... OK.
Preparing image archive ... OK.
Installing SONiC in SONiC
ONIE Installer: platform: x86_64-cisco-8000-r0
onie_platform: x86_64-8101_32h_o-r0
No 8101_32H_O.cpio for x86_64-8101_32h_o-r0 [x86_64-cisco-8000-r0]
Removing old SONiC installation /host/image-202405cz.1.1.0
Installing SONiC to /host/image-202405.1.3.0z
Archive:  fs.zip
   creating: /host/image-202405.1.3.0z/boot/
  inflating: /host/image-202405.1.3.0z/boot/System.map-6.1.0-22-2-amd64
  inflating: /host/image-202405.1.3.0z/boot/vmlinuz-6.1.0-22-2-amd64
  inflating: /host/image-202405.1.3.0z/boot/initrd.img-6.1.0-22-2-amd64
  inflating: /host/image-202405.1.3.0z/boot/config-6.1.0-22-2-amd64
 extracting: /host/image-202405.1.3.0z/fs.squashfs
ONIE_IMAGE_PART_SIZE=32768
EXTRA_CMDLINE_LINUX=
Switch CPU vendor is: GenuineIntel
Switch CPU cstates are: disabled
cp /tmp/tmp.LOOwiQIi3r /boot/efi/EFI/debian/grub.cfg
EXTRA_CMDLINE_LINUX=
Installed SONiC base image SONiC-OS successfully

Command: grub-set-default --boot-directory=/host 0

Command: config-setup backup
Taking backup of current configuration
Executing platform_cisco_cfg-pre_cfg_migration x86_64-8101_32h_o-r0:32x100Gb

Command: mkdir -p /tmp/image-202405.1.3.0z-fs
Command: mount -t squashfs /host/image-202405.1.3.0z/fs.squashfs /tmp/image-202405.1.3.0z-fs
Command: sonic-cfggen -d -y /tmp/image-202405.1.3.0z-fs/etc/sonic/sonic_version.yml -t /tmp/image-202405.1.3.0z-fs/usr/share/sonic/templates/sonic-environment.j2
Command: umount -r -f /tmp/image-202405.1.3.0z-fs
Command: rm -rf /tmp/image-202405.1.3.0z-fs
Command: mkdir -p /tmp/image-202405.1.3.0z-fs
Command: mount -t squashfs /host/image-202405.1.3.0z/fs.squashfs /tmp/image-202405.1.3.0z-fs
Command: mkdir -p /host/image-202405.1.3.0z/rw
Command: mkdir -p /host/image-202405.1.3.0z/work
Command: mkdir -p /tmp/image-202405.1.3.0z-fs
Command: mount overlay -t overlay -o rw,relatime,lowerdir=/tmp/image-202405.1.3.0z-fs,upperdir=/host/image-202405.1.3.0z/rw,workdir=/host/image-202405.1.3.0z/work /tmp/image-202405.1.3.0z-fs
Command: mkdir -p /tmp/image-202405.1.3.0z-fs/var/lib/docker
Command: mount --bind /host/image-202405.1.3.0z/docker /tmp/image-202405.1.3.0z-fs/var/lib/docker
Command: chroot /tmp/image-202405.1.3.0z-fs mount proc /proc -t proc
Command: chroot /tmp/image-202405.1.3.0z-fs mount sysfs /sys -t sysfs
Command: cp /tmp/image-202405.1.3.0z-fs/etc/default/docker /tmp/image-202405.1.3.0z-fs/tmp/docker_config_backup
Command: sh -c echo 'DOCKER_OPTS="$DOCKER_OPTS -H unix:// --storage-driver=overlay2 --bip=240.127.1.1/24 --iptables=false --ipv6=true --fixed-cidr-v6=fd00::/80 "' >> /tmp/image-202405.1.3.0z-fs/etc/default/docker
Command: chroot /tmp/image-202405.1.3.0z-fs /usr/lib/docker/docker.sh start
mount: /sys/fs/cgroup/cpu: cgroup already mounted on /sys/fs/cgroup.
       dmesg(1) may have more information after failed mount system call.
mount: /sys/fs/cgroup/cpuacct: cgroup already mounted on /sys/fs/cgroup.
       dmesg(1) may have more information after failed mount system call.
Command: cp /var/lib/sonic-package-manager/packages.json /tmp/image-202405.1.3.0z-fs/tmp/packages.json
Command: mkdir -p /var/lib/sonic-package-manager/manifests
Command: cp -arf /var/lib/sonic-package-manager/manifests /tmp/image-202405.1.3.0z-fs/var/lib/sonic-package-manager
Command: touch /tmp/image-202405.1.3.0z-fs/tmp/docker.sock
Command: mount --bind /var/run/docker.sock /tmp/image-202405.1.3.0z-fs/tmp/docker.sock
Command: cp /tmp/image-202405.1.3.0z-fs/etc/resolv.conf /tmp/resolv.conf.backup
Command: cp /etc/resolv.conf /tmp/image-202405.1.3.0z-fs/etc/resolv.conf
Command: chroot /tmp/image-202405.1.3.0z-fs sh -c command -v sonic-package-manager
Command: chroot /tmp/image-202405.1.3.0z-fs sonic-package-manager migrate /tmp/packages.json --dockerd-socket /tmp/docker.sock -y
migrating package dhcp-relay
skipping dhcp-relay as installed version is newer
migrating package macsec
skipping macsec as installed version is newer
Command: chroot /tmp/image-202405.1.3.0z-fs /usr/lib/docker/docker.sh stop
Command: mv /tmp/image-202405.1.3.0z-fs/tmp/docker_config_backup /tmp/image-202405.1.3.0z-fs/etc/default/docker
Command: cp /tmp/resolv.conf.backup /tmp/image-202405.1.3.0z-fs/etc/resolv.conf
Command: umount -f -R /tmp/image-202405.1.3.0z-fs
Command: umount -r -f /tmp/image-202405.1.3.0z-fs
Command: rm -rf /tmp/image-202405.1.3.0z-fs
Command: sync

Command: sync

Command: sync

Command: sleep 3

Done
admin@8101-32H-O-1:~$
admin@8101-32H-O-1:~$

```


**Major Steps**:

- Downloads and validates image
- Mounts and extracts `fs.zip`
- Updates GRUB bootloader
- Prepares overlay file system
- Migrates Docker and SONiC packages
- Cleans up temporary mounts and files

**Key Log Entries**:

- `efi not supported`: System lacks EFI validation but continues
- `Installing SONiC to /host/image-...`
- `ONIE Installer platform: x86_64-cisco-8000-r0`
- `Overlay mount`, `docker bind`, `package-manager migrate`

---

## 🔃 Image Management Commands

### `sudo sonic-installer list`

```bash
admin@8101-32H-O-1:~$ sudo sonic-installer list
Current: SONiC-OS-HEAD.1.2.0-7995b757b
Next: SONiC-OS-202405.1.3.0z
Available:
SONiC-OS-202405.1.3.0z
SONiC-OS-HEAD.1.2.0-7995b757b
```




### `sudo sonic-installer set-next-boot SONiC-OS-202405.1.3.0z`

```bash
admin@8101-32H-O-1:~$ sudo sonic-installer set-next-boot SONiC-OS-202405.1.3.0z
Command: grub-reboot --boot-directory=/host 0
```

- Sets the next boot entry via GRUB.
- GRUB setting done with `grub-reboot` command.

---

## 🔄 Final Step

### `sudo reboot`

- Reboots system into the newly installed SONiC image.
- Ensures `/host` GRUB partition boots into the correct version.

---

## 📘 Summary

This interaction walked through detailed SONiC system introspection and image lifecycle management on a Cisco 8101-32H-O switch:

- Validated system platform, hardware, uptime, and image metadata
- Showed full containerized architecture
- Installed and activated a new SONiC image using `sonic-installer`
- Preserved running configuration

🧠 **Useful Links**:

- [SONiC Documentation](https://sonic-net.github.io/SONiC/)
- [SONiC Image Management Guide](https://github.com/Azure/sonic-buildimage/blob/master/image-management/README.md)

