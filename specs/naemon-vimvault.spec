Summary: Naemon VimVault Eventbroker Module
Name: naemon-vimvault
Version: 1.4.2
Release: 4.32%{?dist}
License: GPL-3.0-or-later
Group: Applications/System
URL: https://www.naemon.io/
Packager: Naemon Core Development Team <naemon-dev@monitoring-lists.org>
Vendor: Naemon Core Development Team
Source0: https://github.com/naemon/naemon-vimcrypt-vault-broker/archive/naemon-vimvault-%{version}.tar.gz
BuildRoot: %{_tmppath}/naemon-%{version}-%{release}
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
%setup -q


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
* Thu Oct 24 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1.4.2-4
- added optional macro dist to release

* Fri Nov 05 2021 Sven Nierlein <sven.nierlein@consol.de> 1.3.0-1
- Add packaging
