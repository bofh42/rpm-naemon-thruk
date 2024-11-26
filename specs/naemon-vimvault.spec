%global debug_package %{nil}

Summary:       Naemon VimVault Eventbroker Module
Name:          naemon-vimvault
Version:       1.4.2
Release:       1%{?dist}
License:       GPL-3.0-or-later
Group:         bofh42/addon/naemon

URL:           https://www.naemon.io/
Source0:       https://github.com/naemon/naemon-vimcrypt-vault-broker/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum 5faa3b0892ad0959f1622aa8d0c42014

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: naemon-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: openssl-devel
BuildRequires: gcc-c++


%description
Naemon-VimVault is an eventbroker module for naemon which stores
macros in encrypted files editable with the vim editor.


%prep
echo "%{src0sum}  %{SOURCE0}" | xxh128sum -c

%setup -q -n naemon-vimcrypt-vault-broker-%{version}


%build
test -f configure || ./autogen.sh
%configure \
    --libdir="%{_libdir}/naemon" \
    --with-naemon-config-dir="/etc/naemon/module-conf.d"
%{__make}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

# We don't really want to distribute this
rm %{buildroot}%{_libdir}/naemon/naemon-vimvault/naemon_vimvault.la

%clean
%{__rm} -rf %{buildroot}


%post
exit 0

%preun
exit 0

%postun
exit 0


%files
%attr(0755,naemon,naemon) %dir %{_libdir}/naemon/naemon-vimvault
%attr(0644,root,root) %{_libdir}/naemon/naemon-vimvault/naemon_vimvault.so
%if 0%{?suse_version} >= 1315
%attr(0755,naemon,naemon) %dir %{_sysconfdir}/naemon/
%attr(0755,naemon,naemon) %dir %{_sysconfdir}/naemon/module-conf.d/
%endif
%attr(0644,naemon,naemon) %config(noreplace) %{_sysconfdir}/naemon/module-conf.d/vimvault.cfg

%changelog
* Thu Oct 24 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1.4.2-1
- reset release number to 1 for my own repo
- use git source url and save xxh128 hash in the spec file and check it

* Thu Oct 24 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1.4.2-4
- added optional macro dist to release

* Fri Nov 05 2021 Sven Nierlein <sven.nierlein@consol.de> 1.3.0-1
- Add packaging
