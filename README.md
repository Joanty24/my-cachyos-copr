# My Custom CachyOS Copr Repository

This repository contains the RPM packaging for a custom CachyOS kernel.

## Features
- Based on CachyOS kernel patches.
- Tick rate set to **250Hz**.
- Optimized for x86-64-v3.

## How to use with Copr

1.  Create a new repository on GitHub and push this code to it.
2.  Go to [Copr](https://copr.fedorainfracloud.org/).
3.  Create a new project.
4.  Add a new package:
    - **Source Type**: SCM (Git)
    - **Clone URL**: `https://github.com/YOUR_USERNAME/my-cachyos-copr.git`
    - **Subdirectory**: `sources/kernel-cachyos-custom`
    - **Spec file**: `kernel-cachyos-custom.spec`
5.  Trigger a build!

## Local Testing
You can try building this locally using `mock`:
```bash
fedpkg --dist f41 mockbuild
```
