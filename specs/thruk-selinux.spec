%global debug_package %{nil}

Name:          thruk-selinux
Version:       0.0.1
Release:       1%{?dist}
Summary:       SELinux policies for thruk
License:       GPLv3+
Group:         bofh42/addon/naemon

URL:           https://github.com/bofh42/%{name}
Source0:       %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum 89149872aad0d50c84888f26d3ae2f57

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

install -p -m 644 -D thruk.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/thruk/thruk.pp

# all the script parts are from the epel nrpe rpm
%post
if [ "$1" -le "1" ]; then # First install
   semodule -i %{_datadir}/selinux/packages/thruk/thruk.pp 2>/dev/null || :
   fixfiles -R thruk restore || :
fi

%preun
if [ "$1" -lt "1" ]; then # Final removal
    semodule -r thruk 2>/dev/null || :
    fixfiles -R thruk restore || :
fi

%postun
if [ "$1" -ge "1" ]; then # Upgrade
    # Replaces the module if it is already loaded
    semodule -i %{_datadir}/selinux/packages/thruk/thruk.pp 2>/dev/null || :
fi

%files
%license LICENSE
%doc README.md
%{_datadir}/selinux/packages/thruk/thruk.pp

%changelog
* Thu Oct 24 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- better git source url and save xxh128 hash in the spec file and check it

* Mon Nov 25 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.0.1-1
- initial spec
