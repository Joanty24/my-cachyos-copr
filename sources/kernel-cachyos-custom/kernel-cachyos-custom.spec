# Fedora bits
%define __spec_install_post %{__os_install_post}
%define _build_id_links none
%define _default_patch_fuzz 2
%define _disable_source_fetch 0
%define debug_package %{nil}
%define make_build make %{?_lto_args} %{?_smp_mflags}
%undefine __brp_mangle_shebangs
%undefine _auto_set_build_flags
%undefine _include_frame_pointers

# Linux Kernel Versions
%define _basekver 6.13
%define _stablekver 0
%define _rpmver %{version}-%{release}
%define _kver %{_rpmver}.%{_arch}

%define _tarkver %{version}

# Define the tickrate used by the kernel
%define _hz_tick 250

# Defines the x86_64 ISA level
%define _x86_64_lvl 3

%define _kernel_dir /lib/modules/%{_kver}
%define _devel_dir %{_usrsrc}/kernels/%{_kver}
%define _patch_src https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}

Name:           kernel-cachyos-custom
Summary:        Custom CachyOS Kernel (BORE + %{_hz_tick}Hz)
Version:        %{_basekver}.%{_stablekver}
Release:        1%{?dist}
License:        GPL-2.0-only
URL:            https://cachyos.org

Requires:       kernel-core-uname-r = %{_kver}
Requires:       kernel-modules-uname-r = %{_kver}
Requires:       kernel-modules-core-uname-r = %{_kver}
Provides:       installonlypkg(kernel)

BuildRequires:  bc bison dwarves elfutils-devel flex gcc gettext-devel kmod make openssl openssl-devel perl-Carp perl-devel perl-generators perl-interpreter python3-devel python3-pyyaml python-srpm-macros

Source0:        https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_tarkver}.tar.xz
Source1:        https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos/config
Patch0:         %{_patch_src}/all/0001-cachyos-base-all.patch
Patch1:         %{_patch_src}/sched/0001-bore-cachy.patch

%description
Custom build of CachyOS kernel.

%package core
Summary:        The Linux kernel
Provides:       kernel = %{_rpmver}
Provides:       kernel-core-uname-r = %{_kver}
Requires:       kernel-modules-uname-r = %{_kver}
Provides:       installonlypkg(kernel)

%description core
The kernel-core package contains the Linux kernel.

%package modules
Summary:        Kernel modules for %{name}
Provides:       kernel-modules = %{_rpmver}
Provides:       kernel-modules-uname-r = %{_kver}
Requires:       kernel-uname-r = %{_kver}

%description modules
Kernel modules for the %{name}-core kernel package.

%prep
%setup -q -n linux-%{_tarkver}
cp %{SOURCE1} .config

# Apply patches
%patch -P 0 -p1
%patch -P 1 -p1

scripts/config -e CACHY -e SCHED_BORE
scripts/config --set-str CONFIG_LSM lockdown,yama,integrity,selinux,bpf,landlock
scripts/config -e HZ_%{_hz_tick} --set-val HZ %{_hz_tick}
scripts/config --set-val X86_64_VERSION %{_x86_64_lvl}
%make_build olddefconfig

%build
%make_build EXTRAVERSION=-%{release}.%{_arch} all

%install
install -Dm644 "$(%make_build -s image_name)" "%{buildroot}%{_kernel_dir}/vmlinuz"
%make_build INSTALL_MOD_PATH="%{buildroot}" INSTALL_MOD_STRIP=1 DEPMOD=/doesnt/exist modules_install
rm -rf %{buildroot}%{_kernel_dir}/build
rm -rf %{buildroot}%{_kernel_dir}/source

%files core
%{_kernel_dir}/vmlinuz
%{_kernel_dir}/modules.builtin
%{_kernel_dir}/modules.builtin.modinfo
%{_kernel_dir}/config
%{_kernel_dir}/System.map

%files modules
%dir %{_kernel_dir}
%{_kernel_dir}/modules.order
%{_kernel_dir}/kernel

%files
