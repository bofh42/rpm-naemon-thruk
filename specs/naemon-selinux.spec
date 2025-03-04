%global debug_package %{nil}

%global selinux_42  naemon_42
%global selinux_fix restore /etc/naemon /var/log/naemon /var/cache/naemon /var/lib/naemon

Name:          naemon-selinux
Version:       0.0.4
Release:       1%{?dist}
Summary:       SELinux policies for Naemon
License:       GPLv2+
Group:         bofh42/addon/naemon

URL:           https://github.com/bofh42/%{name}
Source0:       %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum cde0cd5d09d4924873e5abb911700be6

BuildArch:     noarch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: selinux-policy-devel

Requires:      naemon-core
Requires:      policycoreutils

%description
%{summary}

%prep
echo "%{src0sum}  %{SOURCE0}" | xxh128sum -c

%autosetup


%build
make -f /usr/share/selinux/devel/Makefile

%install
rm -rf $RPM_BUILD_ROOT

install -p -m 644 -D %{selinux_42}.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/bofh42/%{selinux_42}.pp

%post
if [ "$1" -le "1" ]; then # First install
  if [ -f /run/.containerenv ]; then
    echo "INFO: %{name} is installed in a container. No SELinux %{selinux_42} module activation is done (just install)"
  else
    semodule -i %{_datadir}/selinux/packages/bofh42/%{selinux_42}.pp 2>/dev/null || :
    fixfiles %{selinux_fix} >/dev/null || :
  fi
fi

%preun
if [ "$1" -lt "1" ]; then # Final removal
  if [ -f /run/.containerenv ]; then
    echo "INFO: %{name} is installed in a container. No SELinux %{selinux_42} module removal is done (just uninstall)"
  else
    semodule -r %{selinux_42} 2>/dev/null || :
    fixfiles %{selinux_fix} >/dev/null || :
  fi
fi

%postun
if [ "$1" -ge "1" ]; then # Upgrade
  if [ -f /run/.containerenv ]; then
    echo "INFO: %{name} is installed in a container. No SELinux %{selinux_42} module update is done (just installed)"
  else
    # Replaces the module if it is already loaded
    semodule -i %{_datadir}/selinux/packages/bofh42/%{selinux_42}.pp 2>/dev/null || :
  fi
fi

%files
%license LICENSE
%doc README.md
%{_datadir}/selinux/packages/bofh42/%{selinux_42}.pp

%changelog
* Tue Mar 04 2025 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.4-1
- upstream update 0.0.4

* Sun Dec 08 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.3-1
- upstream update 0.0.3

* Sat Dec 07 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.2-1
- update from my 1st live server in permissive mode

* Fri Dec 06 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- Requires nameon-core to be sure the fixfiles do exist
- no SELinux module activation/deactivation in a container

* Mon Dec 02 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- use selinux_42 macro for name and bofh42 as package dir
- new selinux_fix macro
- BuildArch noarch

* Sat Nov 30 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- initial spec
