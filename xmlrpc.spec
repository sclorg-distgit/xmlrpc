%global pkg_name xmlrpc
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

Name:       %{?scl_prefix}%{pkg_name}
Version:    3.1.3
Release:    8.15%{?dist}
Epoch:      1
Summary:    Java XML-RPC implementation
License:    ASL 2.0
URL:        http://ws.apache.org/xmlrpc/
Source0:    http://www.apache.org/dist/ws/xmlrpc/sources/apache-xmlrpc-%{version}-src.tar.bz2
# Add OSGi MANIFEST information
Patch0:     %{pkg_name}-client-addosgimanifest.patch
Patch1:     %{pkg_name}-common-addosgimanifest.patch
Patch2:     %{pkg_name}-javax-methods.patch
Patch3:     %{pkg_name}-server-addosgimanifest.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix_maven}maven-resources-plugin
BuildRequires:  %{?scl_prefix_maven}maven-assembly-plugin
BuildRequires:  %{?scl_prefix_maven}maven-source-plugin
BuildRequires:  %{?scl_prefix_maven}maven-site-plugin
BuildRequires:  %{?scl_prefix}ws-commons-util
BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}tomcat-servlet-3.0-api
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  %{?scl_prefix}jakarta-commons-httpclient
BuildRequires:  %{?scl_prefix}apache-commons-logging

BuildArch:    noarch

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:    Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%package common
Summary:    Common classes for XML-RPC client and server implementations
# Provide xmlrpc is not here because it would be useless due to different jar names
# in OSGI manifest
Requires:   %{?scl_prefix}apache-commons-logging

%description common
%{summary}.

%package client
Summary:    XML-RPC client implementation
# in OSGI manifest
Requires:   %{?scl_prefix}jakarta-commons-httpclient

%description client
%{summary}.

%package server
Summary:    XML-RPC server implementation

%description server
%{summary}.

%prep
%setup -q -n apache-%{pkg_name}-%{version}-src
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%patch2 -b .sav
pushd client
%patch0 -b .sav
popd
pushd common
%patch1 -b .sav
popd
pushd server
%patch3 -b .sav
popd

sed -i 's/\r//' LICENSE.txt

%pom_remove_dep jaxme:jaxmeapi

%pom_disable_module dist

%mvn_package :xmlrpc common
%mvn_package :xmlrpc-{common} @1
%mvn_package :xmlrpc-{client} @1
%mvn_package :xmlrpc-{server} @1

%mvn_file :xmlrpc-{common} %{pkg_name}-@1 %{pkg_name}3-@1
%mvn_file :xmlrpc-{client} %{pkg_name}-@1 %{pkg_name}3-@1
%mvn_file :xmlrpc-{server} %{pkg_name}-@1 %{pkg_name}3-@1
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# ignore test failure because server part needs network
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files common -f .mfiles-common
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt

%files client -f .mfiles-client
%files server -f .mfiles-server

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Thu Jul 02 2015 Michael Simacek <msimacek@redhat.com> - 1:3.1.3-8.15
- Fix OSGi manifest metadata (rhbz#1238335)

* Wed Jan 14 2015 Michal Srb <msrb@redhat.com> - 1:3.1.3-8.14
- Fix directory ownership

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1:3.1.3-8.13
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 1:3.1.3-8.12
- Rebuild to regenerate requires

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 1:3.1.3-8.11
- Mass rebuild 2015-01-09

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.10
- Migrate requires and build-requires to rh-java-common

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.9
- Mass rebuild 2014-12-15

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.8
- Rebuild for rh-java-common collection

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.5
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.4
- SCL-ize R on commons-httpclient

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1:3.1.3-8.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-8.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:3.1.3-8
- Mass rebuild 2013-12-27

* Mon Aug 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.1.3-7
- Migrate away from mvn-rpmbuild (#997460)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 1:3.1.3-5
- Remove javax.xml.bind from osgi imports - it's part of the JVM now.
- Drop the ws-jaxme dependency for the same reason.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:3.1.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Oct 20 2012 Peter Robinson <pbrobinson@fedoraproject.org>	3.1.3-2
- xmlrpc v2 had an Epoch so we need one here. Add it back

* Fri Sep 14 2012 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- First release of version 3.x package
