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
%define _basekver 6.18
%define _stablekver 12
%define _rpmver %{version}-%{release}
%define _kver %{_rpmver}.%{_arch}

%if %{_stablekver} == 0
    %define _tarkver %{_basekver}
%else
    %define _tarkver %{version}
%endif

# Define the tickrate used by the kernel
%define _hz_tick 250

# Defines the x86_64 ISA level
%define _x86_64_lvl 3

%define _kernel_dir /lib/modules/%{_kver}
%define _devel_dir %{_usrsrc}/kernels/%{_kver}
%define _patch_src https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}

Name:           kernel-cachyos-custom-stable
Summary:        Custom CachyOS Kernel (BORE + %{_hz_tick}Hz)
Version:        %{_basekver}.%{_stablekver}
Release:        1%{?dist}
License:        GPL-2.0-only
URL:            https://cachyos.org

Requires:       kernel-core-uname-r = %{_kver}
Requires:       kernel-modules-uname-r = %{_kver}
Provides:       installonlypkg(kernel)

BuildRequires:  bc bison dwarves elfutils-devel flex gcc gettext-devel kmod make openssl openssl-devel perl-Carp perl-devel perl-generators perl-interpreter python3-devel python3-pyyaml python-srpm-macros

Source0:        https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_tarkver}.tar.xz
Source1:        https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos/config
Patch0:         %{_patch_src}/all/0001-cachyos-base-all.patch
Patch1:         %{_patch_src}/sched/0001-bore-cachy.patch

%description
Custom build of CachyOS kernel (Stable version).

%package core
Summary:        The Linux kernel
Provides:       kernel = %{_rpmver}
Provides:       kernel-core-uname-r = %{_kver}
Provides:       kernel-uname-r = %{_kver}
Provides:       installonlypkg(kernel)
Requires(preun): /usr/bin/kernel-install
Requires(posttrans): /usr/bin/kernel-install grubby sed dracut

%description core
The kernel-core package contains the Linux kernel.

%package modules
Summary:        Kernel modules for %{name}
Provides:       kernel-modules = %{_rpmver}
Provides:       kernel-modules-uname-r = %{_kver}
Provides:       kernel-modules-core-uname-r = %{_kver}
Provides:       installonlypkg(kernel-module)
Requires:       kernel-uname-r = %{_kver}
Requires(post): /sbin/depmod
Requires(postun): /sbin/depmod
Requires(posttrans): dracut

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
%make_build INSTALL_MOD_PATH="%{buildroot}" INSTALL_MOD_STRIP=1 DEPMOD=/bin/true modules_install
install -Dm644 .config "%{buildroot}%{_kernel_dir}/config"
install -Dm644 System.map "%{buildroot}%{_kernel_dir}/System.map"
rm -rf %{buildroot}%{_kernel_dir}/build
rm -rf %{buildroot}%{_kernel_dir}/source

%post core
mkdir -p /var/lib/rpm-state/kernel
touch /var/lib/rpm-state/kernel/installing_core_%{_kver}

%preun core
entry_type=""
/usr/bin/kernel-install --help | grep -q -- '--entry-type=' && entry_type="--entry-type=type1"
/usr/bin/kernel-install $entry_type remove %{_kver} || exit $?

%posttrans core
rm -f /var/lib/rpm-state/kernel/installing_core_%{_kver}
# Ensure this kernel package is treated as the default type
sed -i 's/^DEFAULTKERNEL=.*/DEFAULTKERNEL=%{name}-core/' /etc/sysconfig/kernel || true
/usr/bin/kernel-install add %{_kver} %{_kernel_dir}/vmlinuz || exit $?
# Explicitly set this specific kernel as default for grubby just in case
MACHINE_ID=$(cat /etc/machine-id 2>/dev/null)
grubby --set-default /boot/${MACHINE_ID}/%{_kver}/linux 2>/dev/null || \
grubby --set-default /boot/vmlinuz-%{_kver} 2>/dev/null || true

%post modules
/sbin/depmod -a %{_kver} || exit $?
if [ ! -f /var/lib/rpm-state/kernel/installing_core_%{_kver} ]; then
    mkdir -p /var/lib/rpm-state/kernel
    touch /var/lib/rpm-state/kernel/need_to_run_dracut_%{_kver}
fi

%postun modules
/sbin/depmod -a %{_kver} || exit $?

%posttrans modules
if [ -f /var/lib/rpm-state/kernel/need_to_run_dracut_%{_kver} ]; then
    rm -f /var/lib/rpm-state/kernel/need_to_run_dracut_%{_kver}
    dracut -f --kver "%{_kver}" || exit $?
fi

%files core
%dir %{_kernel_dir}
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

%changelog
* Tue Feb 24 2026 Custom Kernel Builder <builder@cachyos.org> - 6.18.12-1
- Add changelog to resolve RPM warnings
- Change DEPMOD to /bin/true to silence module installation warnings
