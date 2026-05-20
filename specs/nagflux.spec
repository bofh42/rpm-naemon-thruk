# build command line
# sudo rm -rf ~/.cache/go* ~/go ; rpmbuild -ba nagflux.spec

%define debug_package %{nil}

Name:           nagflux
Version:        0.5.8
Release:        1%{?dist}
Summary:        A connector which transforms performancedata from Nagios/Naemon/Icinga(2) to InfluxDB/Elasticsearch
Group:          42/addon/naemon

License:        GPLv2
Url:            https://github.com/ConSol-Monitoring/nagflux
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# this needs to be updated for every version change
%global src0sum d79e70655648f46cb3468a306d724749

Source7:        https://raw.githubusercontent.com/bofh42/rpm-naemon-thruk/refs/heads/main/sources/nagflux-logrotate
Source8:        https://raw.githubusercontent.com/bofh42/rpm-naemon-thruk/refs/heads/main/sources/nagflux-nagios.cfg
Patch0:         https://raw.githubusercontent.com/bofh42/rpm-naemon-thruk/refs/heads/main/sources/nagflux-0.5.8.patch

BuildRequires:  xxhash
BuildRequires:  make, curl, gcc

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# use OS go or download
%if 0%{?fedora} < 44 && 0%{?rhel} < 11
# download go from https://golang.org/dl/
%define go_ver 1.26.3
%ifarch x86_64
%global go_sha  2b2cfc7148493da5e73981bffbf3353af381d5f93e789c82c79aff64962eb556
%define go_arch amd64
%endif
%ifarch aarch64
%global go_sha  9d89a3ea57d141c2b22d70083f2c8459ba3890f2d9e818e7e933b75614936565
%define go_arch arm64
%endif
%else
BuildRequires:  golang >= 1.26, compiler(go-compiler)
%endif

%description
Nagflux collects data from the NagiosSpoolfileFolder and adds informations from Livestatus.
This data is sent to an InfluxDB, to get displayed by Grafana.
Therefor is the tool Histou gives you the possibility to add Templates to Grafana.

%prep
echo "%{src0sum}  %{SOURCE0}" | xxh128sum -c
%autosetup
%{__mkdir_p} vendor/pkg
cp -rp pkg/nagflux vendor/pkg/

%build
%if "0%{?go_ver}" != "0"
# go download hack
rm -rf %{_builddir}/go%{go_ver} go.tgz || :
wget -O go.tgz https://golang.org/dl/go%{go_ver}.linux-%{go_arch}.tar.gz
echo "%{go_sha}  go.tgz" | sha256sum -c
mkdir %{_builddir}/go%{go_ver}
tar -C %{_builddir}/go%{go_ver} --strip-components=1 -xzf go.tgz
rm -f go.tgz
# use downloaded go
export GOROOT=%{_builddir}/go%{go_ver}
export PATH=${GOROOT}/bin:${PATH}
%endif

make

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m0755 \
    %{buildroot}%{_sysconfdir}/%{name} \
    %{buildroot}%{_sysconfdir}/logrotate.d \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_localstatedir}/spool/%{name} \
    %{buildroot}%{_unitdir}

%{__install} -m0755 -p %{name} %{buildroot}%{_sbindir}/%{name}
%{__install} -m0644 -p config.gcfg.example %{buildroot}%{_sysconfdir}/%{name}/config.gcfg
%{__install} -m0644 -p nagflux.service %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m0644 -p %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -m0644 -p %{SOURCE8} %{buildroot}%{_sysconfdir}/%{name}/

%check
%if "0%{?go_ver}" != "0"
# use donloaded go
export GOROOT=%{_builddir}/go%{go_ver}
export PATH=${GOROOT}/bin:${PATH}
%endif

make test

%{buildroot}%{_sbindir}/%{name} -V | grep "^v%{version} "

%clean
%{__rm} -rf %{buildroot} %{_builddir}/go%{go_ver}

%files
%license LICENSE
%doc CHANGELOG.md README.md config.gcfg.example doc/*
%config(noreplace) %{_sysconfdir}/%{name}/config.gcfg
%config(noreplace) %{_sysconfdir}/%{name}/nagflux-nagios.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%dir %{_localstatedir}/spool/%{name}

%changelog
* Wed May 20 2026 Peter Tuschy <foss+rpm@bofh42.de> - 0.5.2-2
- upstream update 0.5.8
- raised go to 1.26.3
- added patch for config and systemd
- removed extra files for config and systemd
- added source0 checksum + check
- extra source files with download url
- added group 42/addon/naemon

* Wed May 20 2026 Peter Tuschy <foss+rpm@bofh42.de> - 0.5.2-2
- updated go dl from latest rclone spec
- added BuildRequires gcc
- checked build on el10

* Thu Dec 19 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.5.2-1
- initial rpm
