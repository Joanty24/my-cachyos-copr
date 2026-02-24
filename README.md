# My Custom CachyOS Copr Repository

This repository contains the RPM packaging for a custom CachyOS kernel for Fedora, optimized with a 250Hz tick rate and x86-64-v3 instructions. It tracks the official CachyOS kernel releases and automatically rebuilds with custom configuration.

## Features
- **CachyOS Patches**: Includes the BORE scheduler and other CachyOS performance enhancements.
- **Tick Rate**: Reconfigured to `250Hz` for a balance between power efficiency and desktop responsiveness.
- **x86-64-v3**: Compiled with x86-64-v3 ISA level for modern CPU optimizations.
- **Automated Updates**: A GitHub Action automatically checks the upstream CachyOS Copr repository daily, bumps the `.spec` file version to match the latest F43 release, and triggers a new Copr build.
- **Seamless Fedora Integration**: Fully integrates with Fedora's `kernel-install`, `dracut`, and `grubby`. Supports retaining older kernel modules via `installonlypkg`.

## Installation

You can install this custom kernel directly from my Copr repository.

### 1. Enable the Copr repository
```bash
sudo dnf copr enable joanty24/cachyos-custom
```

### 2. Install the kernel
```bash
sudo dnf install kernel-cachyos-custom-stable
```

### 3. Reboot
Reboot your system to start using the new kernel. It will automatically be set as the default boot entry.
```bash
reboot
```

### 4. Verify the changes
After rebooting, you can confirm that the kernel is active and running at 250Hz:

```bash
# Check the kernel version
uname -r

# Verify the tickrate (HZ)
zcat /proc/config.gz | grep CONFIG_HZ
# or check the installed config file:
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
