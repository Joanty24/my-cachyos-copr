# My Custom CachyOS Copr Repository

This repository contains the RPM packaging for a custom CachyOS kernel for Fedora, optimized with a 250Hz tick rate and x86-64-v3 instructions. It tracks the official CachyOS kernel releases and automatically rebuilds with custom configuration.

## Features
- **CachyOS Patches**: Includes the BORE scheduler and other CachyOS performance enhancements.
- **Tick Rate**: Reconfigured to `250Hz` for a balance between power efficiency and desktop responsiveness.
- **x86-64-v3**: Compiled with x86-64-v3 ISA level for modern CPU optimizations.
- **Automated Updates**: A GitHub Action automatically checks the upstream CachyOS Copr repository daily, bumps the `.spec` file version to match the latest F43 release, and triggers a new Copr build.
- **Seamless Fedora Integration**: Fully integrates with Fedora's `kernel-install`, `dracut`, and `grubby`. Supports retaining older kernel modules via `installonlypkg`.

## Checking for CPU support

Check support by the following command:

```bash
/lib64/ld-linux-x86-64.so.2 --help | grep "(supported, searched)"
```

If it does not detect x86\_64\_v3 support, **do not install this kernel**. Otherwise, you will end up with a non-functioning operating system!

## Installation

### Fedora Workstation

#### 1. Enable the Copr repository
```bash
sudo dnf copr enable joanty24/cachyos-custom
```

#### 2. Install the kernel
```bash
sudo dnf install kernel-cachyos-custom-stable kernel-cachyos-custom-stable-devel-matched
```

#### 3. Reboot
```bash
reboot
```

### Fedora Silverblue / Atomic

#### 1. Add the repository
```bash
cd /etc/yum.repos.d/
sudo wget https://copr.fedorainfracloud.org/coprs/joanty24/cachyos-custom/repo/fedora-$(rpm -E %fedora)/joanty24-cachyos-custom-fedora-$(rpm -E %fedora).repo
```

#### 2. Override the stock kernel
```bash
sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos-custom-stable
sudo systemctl reboot
```

## SELinux

If you are using SELinux, enable the following policy to load kernel modules:

```bash
sudo setsebool -P domain_kernel_load_modules on
```

## Verify the installation

After rebooting, confirm the kernel is active and running at 250Hz:

```bash
# Check the kernel version
uname -r

# Verify the tickrate (HZ)
grep CONFIG_HZ /lib/modules/$(uname -r)/config
```

## How to use with Copr (For Developers)

If you want to fork this repository and build it in your own Copr:

1. Go to [Copr](https://copr.fedorainfracloud.org/).
2. Create a new project.
3. Add a new package:
   - **Source Type**: SCM (Git)
   - **Clone URL**: `https://github.com/YOUR_USERNAME/my-cachyos-copr.git`
   - **Subdirectory**: `sources/kernel-cachyos-custom-stable`
   - **Spec file**: `kernel-cachyos-custom-stable.spec`
4. Trigger a build!
