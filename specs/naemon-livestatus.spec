%global debug_package %{nil}

Summary:       Naemon Livestatus Eventbroker Module
Name:          naemon-livestatus
Version:       1.4.3
Release:       1%{?dist}
License:       GPL-2.0-only
Group:         bofh42/addon/naemon

URL:           https://www.naemon.io/
Source0:       https://github.com/naemon/%{name}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum b3869fff1078f24d20896346d8546bc6

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: naemon-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: gcc-c++
%if 0%{?el8}
BuildRequires: gdb-headless
%endif


%description
Naemon-livestatus is an eventbroker module for naemon which allows
external programs to use the running Nagios daemon as a specialized
database.


%prep
echo "%{src0sum}  %{SOURCE0}" | xxh128sum -c

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
rm -f %{buildroot}%{_libdir}/naemon/naemon-livestatus/livestatus.la

install -d %{buildroot}%{_localstatedir}/log/naemon

%clean
%{__rm} -rf %{buildroot}


%post
case "$*" in
  2)
    # Upgrading so try and restart if already running
    if [ -e /etc/naemon/naemon.cfg ]; then
      # livestatus configuration has been moved to single drop dir file
      sed -i /etc/naemon/naemon.cfg -e 's~^\s*\(broker_module=/usr/lib[0-9]*/naemon/naemon-livestatus/livestatus.so.*\)~#\1~'
    fi
  ;;
  1)
    # First installation, no acton required
    :
  ;;
  *) echo case "$*" not handled in postun
esac
%if 0%{?use_systemd}
  systemctl condrestart naemon.service
%else
  /etc/init.d/naemon condrestart &>/dev/null || :
%endif
exit 0

%preun
case "$*" in
  0)
    # POSTUN
    rm -f /var/log/naemon/livestatus.log
    ;;
  1)
    # POSTUPDATE
    ;;
  *) echo case "$*" not handled in postun
esac
exit 0

%postun
case "$*" in
  0)
    # POSTUN
    if [ -e /etc/naemon/naemon.cfg ]; then
      sed -i /etc/naemon/naemon.cfg -e 's~^\s*\(broker_module=/usr/lib[0-9]*/naemon/naemon-livestatus/livestatus.so.*\)~#\1~'
    fi
    rm -f /var/cache/naemon/live
    ;;
  1)
    # POSTUPDATE
    ;;
  *) echo case "$*" not handled in postun
esac
exit 0


%files
%attr(0755,root,root) %{_bindir}/unixcat
%attr(0755,naemon,naemon) %dir %{_libdir}/naemon/naemon-livestatus
%attr(0644,root,root) %{_libdir}/naemon/naemon-livestatus/livestatus.so
%attr(0755,naemon,naemon) %dir %{_localstatedir}/log/naemon
%if 0%{?suse_version} >= 1315
%attr(0755,naemon,naemon) %dir %{_sysconfdir}/naemon/
%attr(0755,naemon,naemon) %dir %{_sysconfdir}/naemon/module-conf.d/
%endif
%attr(0644,naemon,naemon) %config(noreplace) %{_sysconfdir}/naemon/module-conf.d/livestatus.cfg

%changelog
* Mon Mar 03 2025 Peter Tuschy <foss+rpm@bofh42.de> - 1.4.3-1
- upstream update

* Tue Nov 26 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1.4.2-1
- reset release number to 1 for my own repo
- use git source url and save xxh128 hash in the spec file and check it

* Thu Oct 24 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1.4.2-15
- added optional macro dist to release

* Tue Sep 19 2017 Sven Nierlein <sven.nierlein@consol.de> 1.0.7-1
- Decouple core and livestatus
