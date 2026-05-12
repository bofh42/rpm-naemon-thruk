Summary:       Thruk perl libraries
Name:          libthruk
Version:       3.24
Release:       1%{?dist}
License:       GPL-2.0-or-later
Group:         42/addon/naemon

URL:           http://www.thruk.org/
Source0:       https://github.com/sni/thruk_libs/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum 72d6cf46d1b691ddf2d234cfcb538cb3

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: xxhash
BuildRequires: make
BuildRequires: rsync
BuildRequires: gcc
BuildRequires: perl
BuildRequires: perl(Bit::Vector)
BuildRequires: perl(Cpanel::JSON::XS)
BuildRequires: perl(Date::Calc)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(ExtUtils::Install)
BuildRequires: perl(HTTP::Request)
BuildRequires: perl(IO::Scalar)
BuildRequires: perl(LWP::Protocol::https)
BuildRequires: perl(LWP::UserAgent)
BuildRequires: perl(Module::Install)
BuildRequires: perl(XML::Parser)

# rhel / rocky / alma / fedora
%if 0%{?rhel} || 0%{?rocky} || 0%{?almalinux} || 0%{?fedora}
BuildRequires: perl-devel
%endif

# rhel / rocky / alma
%if 0%{?rhel} || 0%{?rocky} || 0%{?almalinux}
BuildRequires: epel-release
%endif

Requires:      yumrepo-epel-thruk
Requires:      perl(Bit::Vector)
Requires:      perl(Cpanel::JSON::XS)
Requires:      perl(Crypt::Rijndael)
Requires:      perl(Date::Calc)
Requires:      perl(Date::Manip)
Requires:      perl(DBD::mysql)
Requires:      perl(DBI)
Requires:      perl(FCGI)
Requires:      perl(GD)
Requires:      perl(HTML::Entities)
Requires:      perl(HTTP::Request)
Requires:      perl(IO::Scalar)
Requires:      perl(IO::Socket::IP)
Requires:      perl(IO::Socket::SSL)
Requires:      perl(IO::String)
Requires:      perl(Log::Log4perl)
Requires:      perl(LWP::Protocol::https)
Requires:      perl(LWP::UserAgent)
Requires:      perl(MIME::Lite)
Requires:      perl(Module::Load)
Requires:      perl(Net::HTTP)
Requires:      perl(Net::SSLeay)
Requires:      perl(parent)
Requires:      perl(Plack)
Requires:      perl(Plack::Handler::FCGI)
Requires:      perl(Plack::Util)
Requires:      perl(Plack::Test)
Requires:      perl(Pod::Usage)
Requires:      perl(Socket)
Requires:      perl(Storable)
Requires:      perl(Template)
Requires:      perl(Thread::Queue)
Requires:      perl(threads)
Requires:      perl(Tie::IxHash)
Requires:      perl(Time::HiRes)
Requires:      perl(URI::Escape)
Requires:      perl(XML::Parser)

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

%clean
%{__rm} -rf %{buildroot}

%files
%attr(-,root,root) %{_libdir}/thruk

%changelog
* Tue May 12 2026 Peter Tuschy <foss+rpm@bofh42.de> - 3.24-1
- now based on upstream spec 3.24
- group changed to 42/addon/naemon
- use git source url and save xxh128 hash in the spec file and check it
- yumrepo-epel-thruk for perl dependencies

* Fri Aug 22 2025 Sven Nierlein <sven.nierlein@consol.de> 3.24-1
- Migrate to use system perl modules whenever possible

* Tue Apr 28 2026 Peter Tuschy <foss+rpm@bofh42.de> - 3.22.2-1
- upstream update 3.22.2

* Tue Mar 24 2026 Peter Tuschy <foss+rpm@bofh42.de> - 3.20-2
- changed group to 42/addon/naemon for my new repo scripts

* Mon Mar 03 2025 Peter Tuschy <foss+rpm@bofh42.de> - 3.20-1
- upstream update

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
