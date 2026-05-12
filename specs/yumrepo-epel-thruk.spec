
%define yumname Thruk
%define yumrepo thruk
# to create the list in a container
# sudo dnf install libthruk
# sudo dnf list installed | grep @epel | awk '{ print $1 }' | awk -F. '{ print $1 }' | sort | xargs | sed 's| |,|g
%define yumincl perl-Apache-LogFormat-Compiler,perl-AppConfig,perl-B-Hooks-EndOfScope,perl-CGI-Compile,perl-CGI-Emulate-PSGI,perl-Class-Data-Inheritable,perl-Cookie-Baker,perl-Cpanel-JSON-XS,perl-Crypt-Rijndael,perl-Devel-Caller,perl-Devel-LexAlias,perl-Devel-StackTrace-AsHTML,perl-Dist-CheckConflicts,perl-Email-Date-Format,perl-Eval-Closure,perl-Exception-Class,perl-FCGI-ProcManager,perl-Filesys-Notify-Simple,perl-GD,perl-Hash-MultiValue,perl-HTTP-Entity-Parser,perl-HTTP-Headers-Fast,perl-HTTP-MultiPartParser,perl-HTTP-Parser-XS,perl-Image-Base,perl-Image-Info,perl-Image-Xbm,perl-Image-Xpm,perl-JSON-MaybeXS,perl-Lexical-SealRequireHints,perl-Lexical-Var,perl-Linux-Inotify2,perl-Log-Dispatch,perl-Log-Dispatch-FileRotate,perl-Log-Log4perl,perl-Mail-Sender,perl-Mail-Sendmail,perl-MIME-Lite,perl-MIME-Types,perl-Module-Implementation,perl-Module-Refresh,perl-namespace-autoclean,perl-namespace-clean,perl-Package-Stash,perl-Package-Stash-XS,perl-PadWalker,perl-Params-ValidationCompiler,perl-Plack,perl-Plack-Handler-FCGI,perl-Plack-Test,perl-Pod-POM,perl-POSIX-strftime-Compiler,perl-Ref-Util,perl-Ref-Util-XS,perl-Specio,perl-Stream-Buffered,perl-Sub-Name,perl-Template-Toolkit,perl-Test-SharedFork,perl-Test-TCP,perltidy,perl-Variable-Magic,perl-WWW-Form-UrlEncoded,rgb
%define gpgkey https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-%{rhel}
%define yumkey /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{rhel}-%{yumrepo}

# EPEL cant handle releasver minor versions, so pinning it to major version
%if 0%{?rhel}
%define osrelease %{rhel}
%endif

%if 0%{?fedora}
%define osrelease $releasever
%endif

Summary:    yumrepo EPEL %{yumname}
Name:       yumrepo-epel-%{yumrepo}
Epoch:      1
Version:    %{?rhel}%{?fedora}
Release:    2.0%{?dist}
Group:      42/extras
License:    multiple
BuildRoot:  %{_tmppath}/%{rpmwho}-release-root

BuildArch:  noarch

%description
part of EPEL as yum repo 42-epel-%{yumrepo}

%install
mkdir -p $RPM_BUILD_ROOT/etc/yum.repos.d
mkdir -p $RPM_BUILD_ROOT/etc/pki/rpm-gpg
curl -sSf %{gpgkey} >$RPM_BUILD_ROOT%{yumkey}

cat <<'EOF' >$RPM_BUILD_ROOT/etc/yum.repos.d/42-epel-%{yumrepo}.repo
[42-epel-%{yumrepo}]
name=EPEL %{osrelease} - %{yumname}
metalink=https://mirrors.fedoraproject.org/metalink?repo=epel-%{osrelease}&arch=$basearch&infra=$infra&content=$contentdir
enabled=1
gpgcheck=1
gpgkey=file://%{yumkey}
includepkgs=%{yumincl}

[42-epel-%{yumrepo}-source]
name=EPEL %{osrelease} - %{yumname} - Source
metalink=https://mirrors.fedoraproject.org/metalink?repo=epel-source-%{osrelease}&arch=$basearch&infra=$infra&content=$contentdir
enabled=0
gpgkey=file://%{yumkey}
gpgcheck=1
includepkgs=%{yumincl}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
# import gpg key if systemd is running
if [ -d /run/systemd/system -a -x /bin/systemd-run ]; then
  systemd-run --on-active=2 --timer-property=AccuracySec=100m rpm --import %{yumkey}
fi

%files
%defattr(-,root,root)
%attr(0644,root,root) /etc/yum.repos.d/42-epel-%{yumrepo}.repo
%attr(0644,root,root) %{yumkey}

%changelog
* Sun Nov 09 2025 Peter Tuschy <foss+rpm@bofh42.de> - 1:%{version}-2.0
- changed for el10
- changed group 42/extras

* Sun Nov 17 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1:%{version}-1.0
- EPEL cant handle releasver minor versions, so pinning it to major version
- Epoch 1, Version os major, release 1.0

* Wed May 15 2024 Peter Tuschy <foss+rpm@bofh42.de> - 1.0-1
- initial verson
