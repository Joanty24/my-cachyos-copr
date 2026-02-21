# My Custom CachyOS Copr Repository

This repository contains the RPM packaging for a custom CachyOS kernel, optimized with a 250Hz tick rate and x86-64-v3 instructions.

## Versions
We provide two tracks:
- **Stable (`kernel-cachyos-custom-stable`)**: Tracks the exact kernel version as the official CachyOS Copr repository (currently `6.18.12`).
- **Edge (`kernel-cachyos-custom-edge`)**: Tracks the latest stable upstream branch of the CachyOS patches (currently `6.19.3`).

## How to use with Copr

1. Go to [Copr](https://copr.fedorainfracloud.org/).
2. Create a new project or select an existing one.
3. Add a new package for whichever track you want to build:
   - **Source Type**: SCM (Git)
   - **Clone URL**: `https://github.com/YOUR_USERNAME/my-cachyos-copr.git`
   
   **For Stable:**
   - **Subdirectory**: `sources/kernel-cachyos-custom-stable`
   - **Spec file**: `kernel-cachyos-custom-stable.spec`
   
   **For Edge:**
   - **Subdirectory**: `sources/kernel-cachyos-custom-edge`
   - **Spec file**: `kernel-cachyos-custom-edge.spec`

4. Trigger a build!
