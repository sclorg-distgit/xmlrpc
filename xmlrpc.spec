%{?scl:%scl_package xmlrpc}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}xmlrpc
Version:        3.1.3
Release:        8.4%{?dist}
Epoch:          1
Summary:        Java XML-RPC implementation
License:        ASL 2.0
URL:            http://ws.apache.org/xmlrpc/
BuildArch:      noarch

Source0:        http://www.apache.org/dist/ws/xmlrpc/sources/apache-xmlrpc-%{version}-src.tar.bz2
Patch0:         %{pkg_name}-client-addosgimanifest.patch
Patch1:         %{pkg_name}-common-addosgimanifest.patch
Patch2:         %{pkg_name}-javax-methods.patch
Patch3:         %{pkg_name}-server-addosgimanifest.patch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache:apache:pom:)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-httpclient:commons-httpclient)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-logging:commons-logging)
BuildRequires:  %{?scl_prefix_java_common}mvn(javax.servlet:servlet-api)
BuildRequires:  %{?scl_prefix_java_common}ws-commons-util

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:    Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package common
Summary:    Common classes for XML-RPC client and server implementations

%description common
%{summary}.

%package client
Summary:    XML-RPC client implementation

%description client
%{summary}.

%package server
Summary:    XML-RPC server implementation

%description server
%{summary}.

%prep
%setup -q -n apache-%{pkg_name}-%{version}-src
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

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_disable_module dist
%pom_remove_dep jaxme:jaxmeapi common
%mvn_file :{*} @1
%mvn_package :*-common %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# FIXME: ignore test failure because server part needs network
%mvn_build -s -- -Dmaven.test.failure.ignore=true
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files common -f .mfiles-%{pkg_name}
%doc LICENSE.txt NOTICE.txt

%files client -f .mfiles-%{pkg_name}-client

%files server -f .mfiles-%{pkg_name}-server

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Mon May 11 2015 Mat Booth <mat.booth@redhat.com> - 1:3.1.3-8.4
- Resolves: rhbz#1219013 - Fails to build from source

* Thu Jul 10 2014 Sami Wagiaalla <swagiaal@redhat.com> - 1:3.1.3-8.3
- Add OSGi info for xmlrpc-server jar.
- export o.a.xmlrpc from xmlrpc-client jar.

* Tue May 27 2014 Mat Booth <mat.booth@redhat.com> - 1:3.1.3-8.1
- SCL-ise for dts3.

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.1.3-8
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:3.1.3-6
- Update to current packaging guidelines

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 1:3.1.3-5
- Remove javax.xml.bind from osgi imports - it's part of the JVM now.
- Drop the ws-jaxme dependency for the same reason.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:3.1.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Oct 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.1.3-2
- xmlrpc v2 had an Epoch so we need one here. Add it back

* Fri Sep 14 2012 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- First release of version 3.x package
