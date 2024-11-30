%global debug_package %{nil}

Name:          naemon-selinux
Version:       0.0.1
Release:       1%{?dist}
Summary:       SELinux policies for Naemon
License:       GPLv2+
Group:         bofh42/addon/naemon

URL:           https://github.com/bofh42/%{name}
Source0:       %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum 233f4d78f6c49fdb06544745a924d373

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: selinux-policy-devel

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

install -p -m 644 -D naemon_42.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/naemon/naemon_42.pp

# all the script parts are from the epel nrpe rpm and adjusted
%post
if [ "$1" -le "1" ]; then # First install
  semodule -i %{_datadir}/selinux/packages/naemon/naemon_42.pp 2>/dev/null || :
  fixfiles restore /etc/naemon /var/log/naemon /var/cache/naemon /var/lib/naemon >/dev/null || :
fi

%preun
if [ "$1" -lt "1" ]; then # Final removal
  semodule -r naemon_42 2>/dev/null || :
  fixfiles restore /etc/naemon /var/log/naemon /var/cache/naemon /var/lib/naemon >/dev/null || :
fi

%postun
if [ "$1" -ge "1" ]; then # Upgrade
    # Replaces the module if it is already loaded
    semodule -i %{_datadir}/selinux/packages/naemon/naemon_42.pp 2>/dev/null || :
fi

%files
%license LICENSE
%doc README.md
%{_datadir}/selinux/packages/naemon/naemon_42.pp

%changelog
* Sat Nov 30 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- initial spec
