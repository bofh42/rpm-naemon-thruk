
Summary:       Thruk perl libraries
Name:          libthruk
Version:       3.14
Release:       1%{?dist}
License:       GPL-2.0-or-later
Group:         bofh42/addon/naemon

URL:           http://www.thruk.org/
Source0:       https://github.com/sni/thruk_libs/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum e0f7c3ca7c22ed528072c253ce39b5a8

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: gd-devel > 1.8
BuildRequires: zlib-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: mysql-devel
BuildRequires: perl
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: binutils
BuildRequires: gcc
BuildRequires: chrpath
BuildRequires: rsync

Requires: gd

# sles
%if %{defined suse_version}
BuildRequires: libexpat-devel
BuildRequires: fontconfig-devel
BuildRequires: xorg-x11-libXpm-devel
# sles 12
%if 0%{?suse_version} >= 1315
BuildRequires: libpng16-devel
BuildRequires: libtiff-devel
BuildRequires: libvpx-devel
Requires: libjpeg62
%else
# sles 11
BuildRequires: freetype2-devel
%endif
%endif

# centos
%if 0%{?el6}
BuildRequires: perl-devel
BuildRequires: expat-devel
%endif
%if 0%{?el7}
BuildRequires: perl(Locale::Maketext::Simple)
BuildRequires: perl-devel
Requires: perl(Data::Dumper)
Requires: perl(Digest)
%endif
%if 0%{?el8}
BuildRequires: perl-devel
BuildRequires: expat-devel
%endif
%if 0%{?el9}
BuildRequires: perl-devel
BuildRequires: expat-devel
# to remove warnings at build time this bunch of perl rpms is needed (not sure if it is Requires too)
# you find this in my bofh42/extras repo
BuildRequires: perl(Mock::Config)
# part of the os
BuildRequires: perl(Module::ScanDeps), perl(IO::CaptureOutput), perl(Mail::Address), perl(CGI)
BuildRequires: perl(IO::HTML), perl(Apache::LogFormat::Compiler), perl(Devel::StackTrace)
BuildRequires: perl(Devel::StackTrace::AsHTML), perl(Filesys::Notify::Simple), perl(File::Listing)
BuildRequires: perl(HTTP::Daemon), perl(WWW::RobotRules)
# this is from testing and it did complain abount missing modules
Requires: perl(threads), perl(File::Copy), perl(Time::HiRes)
%endif

# fedora
%if 0%{?fedora}
BuildRequires: perl-devel
BuildRequires: expat-devel
%endif

# disable creating useless empty debug packages
%define debug_package %{nil}

# disable automatic requirements
AutoReqProv:   no

%description
Thruk is a multibackend monitoring webinterface which currently
supports Nagios, Icinga and Shinken as backend using the Livestatus
API. It is designed to be a 'dropin' replacement and covers almost
all of the original features plus adds additional enhancements for
large installations.

%prep
echo "%{src0sum}  %{SOURCE0}" | xxh128sum -c
%setup -q -n thruk_libs-%{version}

%build
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}" LIBDIR="%{_libdir}/thruk/"
%if %{defined suse_version}
%{__make} installbuilddeps DESTDIR="%{buildroot}" LIBDIR="%{_libdir}/thruk/"
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%attr(-,root,root) %{_libdir}/thruk

%changelog
* Fri Dec 06 2024 Peter Tuschy <foss+rpm@bofh42.de> - 3.14-1
- added el9 Requires perl(Time::HiRes)

* Sat Nov 30 2024 Peter Tuschy <foss+rpm@bofh42.de> - 3.14-1
- reduced extra Requires for el9 to perl(threads), perl(File::Copy)

* Tue Nov 26 2024 Peter Tuschy <foss+rpm@bofh42.de> - 3.14-1
- reset release number to 1 for my own repo
- use git source url and save xxh128 hash in the spec file and check it
- added a bunch of perl modules for build and install on el9

* Thu Oct 24 2024 Peter Tuschy <foss+rpm@bofh42.de> - 3.14-19
- added optional macro dist to release

* Mon Jul 13 2015 Sven Nierlein <sven.nierlein@consol.de> 2.00-1
- Initial libs package
