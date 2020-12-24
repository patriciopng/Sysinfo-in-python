from pathlib import Path
import platform
import re

arch = platform.machine() #Arch
systemname = platform.system() #SytemName
kernelversion = platform.release() #kernel version
hostname = platform.node()

with open("/proc/meminfo") as fileOpen: MemFile = fileOpen.read()
fileOpen.closed

memTotal = re.search("MemTotal:.*\n", MemFile)
memFree = re.search("MemFree:.*\n", MemFile)
buffers = re.search("Buffers:.*\n", MemFile)
cached = re.search("Cached:.*\n", MemFile)
slab = re.search("Slab:.*\n", MemFile)

memTotal = int(re.sub("[^0-9]", "", memTotal.group(0)))
memFree = int(re.sub("[^0-9]", "", memFree.group(0)))
buffers = int(re.sub("[^0-9]", "", buffers.group(0)))
cached = int(re.sub("[^0-9]", "", cached.group(0)))
slab = int(re.sub("[^0-9]", "", slab.group(0)))

memUsed = memTotal - memFree - buffers - cached - slab
memTotal = float(memTotal/1024)
memUsed = float(memUsed/1024)

if Path("/usr/include/gnu").exists(): libc = "glibc"
else:
    libc = "Musl"

if Path("/usr/bin/pulseaudio").exists(): audio = "Pulseaudio"
else:
    audio = "Alsa"

if Path("/etc/portage/make.conf").exists():
    with open("/etc/portage/make.conf") as fileOpen: confFile = fileOpen.read()
    fileOpen.closed
    cflags = re.search("CFLAGS=.*", confFile)
    cxxflags = re.search("CXXFLAGS=.*", confFile)
    cflags = cflags.group(0)
    cxxflags = cxxflags.group(0)
else:
    cflags = "install"
    cxxflags = "Gentoo"

if Path("/sbin/openrc").exists(): Init = "OpenRC"
elif Path("/etc/runit").exists(): Init = "Runit"
elif Path("/etc/systemd").exists(): Init = "SystemD"
else: 
    Init = "not supported"

if Path("/etc/default/grub").exists(): boot = "GRUB"
elif Path("/sbin/lilo").exists(): boot = "Lilo"
elif Path("/boot/extlinux").exists(): boot = "Syslinux(extlinux)"
else:
    boot = "not supported"

if Path("/etc/NetworkManager").exists(): Wireless = "NetworkManager"
elif Path("/etc/wpa_supplicant").exists(): Wireless = "wpa_supplicant"
else:
    Wireless = "Dont use"

if Path("/etc/dhcpcd.conf").exists(): dhcp = "dhcpcd"
elif Path("/etc/dhcp").exists(): dhcp = "dhclient"
else:
    dhcp = ""

if Path("/etc/dhcpcd.conf","/etc/dhcp").exists(): dhcp = "dhcpcd + dhclient"
elif Path("/usr/sbin/sdhcp").exists(): dhcp = "sdhcp"
else:
    dhcp = ""

with open("/etc/os-release") as fileOpen: OsFile = fileOpen.read()
fileOpen.closed

dist = re.search("NAME=.*", OsFile)
dist = dist.group(0)

with open("/proc/cpuinfo") as fileOpen: CpuFile = fileOpen.read()
fileOpen.closed

cpu = re.search("model name.*", CpuFile)
cpu = cpu.group(0)

print("\nhostname:   {}".format(hostname),
      "\nArch:       {}".format(arch),
      "\nProc:       {}".format(cpu),
      "\nKernel:     {} {}".format(systemname,kernelversion),
      "\nDistro:     {}".format(dist),
      "\nLibc:       {}".format(libc),
      "\nMem:        {:.0f}MiB / {:.0f}MiB".format(memUsed,memTotal),
      "\nAudio:      {}".format(audio),
      "\nC:          {}".format(cflags),
      "\nCPP:        {}".format(cxxflags),
      "\nInit:       {}".format(Init),
      "\nBootloader: {}".format(boot),
      "\ndhcpc:      {}".format(dhcp),
      "\nWireless:   {}".format(Wireless),
      "\n")
