# build command line
# sudo rm -rf ~/.cache/go* ~/go ; rpmbuild -ba nagflux.spec

%define debug_package %{nil}

Name:           nagflux
Version:        0.5.2
Release:        1%{?dist}
Summary:        A connector which transforms performancedata from Nagios/Naemon/Icinga(2) to InfluxDB/Elasticsearch

License:        GPLv2
Url:            https://github.com/ConSol-Monitoring/nagflux
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Source5:        nagflux-config.gcfg
Source6:        nagflux.service
Source7:        nagflux-logrotate
Source8:        nagflux-nagios.cfg

BuildRequires:  make, curl

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# use OS go or download
%if 0%{?fedora} < 38 || 0%{?rhel} < 10
# download go from https://golang.org/dl/
%define go_ver 1.22.10
%ifarch x86_64
%global go_sha  736ce492a19d756a92719a6121226087ccd91b652ed5caec40ad6dbfb2252092
%define go_arch amd64
%endif
%ifarch aarch64
%global go_sha  5213c5e32fde3bd7da65516467b7ffbfe40d2bb5a5f58105e387eef450583eec
%define go_arch arm64
%endif
%else
BuildRequires:  golang >= 1.22, compiler(go-compiler)
%endif

%description
Nagflux collects data from the NagiosSpoolfileFolder and adds informations from Livestatus.
This data is sent to an InfluxDB, to get displayed by Grafana.
Therefor is the tool Histou gives you the possibility to add Templates to Grafana.

%prep
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
%{__install} -m0644 -p %{SOURCE5} %{buildroot}%{_sysconfdir}/%{name}/config.gcfg
%{__install} -m0644 -p %{SOURCE6} %{buildroot}%{_unitdir}/%{name}.service
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
%doc CHANGELOG.md README.md config.gcfg.example
%config(noreplace) %{_sysconfdir}/%{name}/config.gcfg
%config(noreplace) %{_sysconfdir}/%{name}/nagflux-nagios.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%dir %{_localstatedir}/spool/%{name}

%changelog
* Thu Dec 19 2024 Peter Tuschy <foss+rpm@bofh42.de> - 0.5.2-1
- initial rpm
