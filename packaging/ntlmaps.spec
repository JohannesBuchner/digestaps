# ntlmaps.spec
# Copyright (C) 2004 Darryl Dixon <esrever_otua@pythonhacker.is-a-geek.net>
# This program may be freely redistributed under the terms of the GNU GPLv2+
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name: ntlmaps
Version: 1.0
Release: 1%{?dist}
Summary: NTLM Authorization Proxy Server

Group: Applications/Internet
License: GPLv2+
URL: http://ntlmaps.sourceforge.net
Source0:        http://downloads.sourceforge.net/ntlmaps/%{name}-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: python-devel >= 1.5.2, dos2unix
BuildArch: noarch
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description
NTLM Authorization Proxy Server is a proxy software that allows you to
authenticate via a Microsoft Proxy Server using the proprietary NTLM
protocol. Since version 0.9.5 APS has an ability to behave as a
standalone proxy server and authenticate http clients at web servers
using NTLM method.

%prep
%setup -q

%build
%{__python} packaging/setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} packaging/setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
dos2unix COPYING doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING doc/*
%{python_sitelib}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/server.cfg
%{_bindir}/%{name}*
%{_sysconfdir}/rc.d/init.d/%{name}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%changelog
* Mon Apr 13 2009 Matt Domsch <mdomsch@fedoraproject.org> - 1.0-1
- minor cleanups.
- finally a 1.0 release!

* Tue Oct 21 2008 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.9.8-1
- cleanup for Fedora packaging

* Tue Jul 05 2005 Darryl Dixon <esrever_otua@pythonhacker.is-a-geek.net>
  [ntlmaps-0.9.9.6]
- Mark server.cfg as config file

* Fri Jun 10 2005 Darryl Dixon <esrever_otua@pythonhacker.is-a-geek.net>
  [ntlmaps-0.9.9.4]
- Move server.cfg to %%{_sysconfdir} for better FHS compliance

* Thu Feb 24 2005 Darryl Dixon <esrever_otua@pythonhacker.is-a-geek.net>
  [ntlmaps-0.9.9.3]
- Update for moved file locations in source dir
- Use %%{ntlmaps_dir}
- Move server.cfg to %%{_localstatedir}%{ntlmaps_dir} (/var/opt/ntlmaps)

* Wed Feb 23 2005 Darryl Dixon <esrever_otua@pythonhacker.is-a-geek.net>
  [ntlmaps-0.9.9.2]
- Initial release of .spec file
