%global debug_package %{nil}

%global selinux_42  thruk_42
%global selinux_fix restore /etc/thruk /var/log/thruk /var/cache/thruk /var/lib/thruk

Name:          thruk-selinux
Version:       0.0.3
Release:       1%{?dist}
Summary:       SELinux policies for thruk
License:       GPLv2+
Group:         bofh42/addon/naemon

URL:           https://github.com/bofh42/%{name}
Source0:       %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum 5b228f449a3a1e743190a0b313c197e1

BuildArch:     noarch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: selinux-policy-devel

Requires:      thruk-base
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
* Sun Dec 08 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.3-1
- upstream update 0.0.3

* Sat Dec 07 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.2-1
- update from my 1st live server in permissive mode

* Fri Dec 05 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- Requires thruk-base to be sure the fixfiles do exist
- no SELinux module activation/deactivation in a container

* Mon Dec 02 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- use selinux_42 macro for name and bofh42 as package dir
- new selinux_fix macro
- BuildArch noarch

* Sat Nov 30 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- from scratch new git repo
- fixfiles with dir not rpm

* Tue Nov 26 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- better git source url and save xxh128 hash in the spec file and check it

* Mon Nov 25 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- initial spec
