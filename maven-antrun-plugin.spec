%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-antrun-plugin
Version:        1.7
Release:        6.1%{?dist}
Summary:        Maven AntRun Plugin

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-antrun-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip 

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)


Obsoletes: maven2-plugin-antrun <= 0:2.0.8
Provides: maven2-plugin-antrun = 1:%{version}-%{release}

%description
This plugin provides the ability to run Ant tasks from within Maven.
It is even possible to embed Ant scripts in the POM.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q 

%pom_add_dep org.apache.maven:maven-compat

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Sep 02 2013 Michal Srb <msrb@redhat.com> - 1.7-6
- Adapt to current guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.7-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 1 2011 Alexander Kurtakov <akurtako@redhat.com> 1.7-1
- Update to 1.7 upstream release.

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 1.6-4
- Build with maven 3.x.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Alexander Kurtakov <akurtako@redhat.com> 1.6-2
- Make it work with ant 1.8.2.

* Thu Oct 14 2010 Alexander Kurtakov <akurtako@redhat.com> 1.6-1
- Update to 1.6.

* Mon Sep 20 2010 Alexander Kurtakov <akurtako@redhat.com> 1.5-1
- Update to 1.5.
- Use upstream tarball.
- Add License and readme as doc.

* Tue Aug 31 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4-4
- Fix runtime issue of not finding ant-launcher.

* Tue Aug 31 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4-3
- Add patch to fix build.

* Fri May 28 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4-2
- Add provides/obsoletes.

* Thu May 27 2010 Alexander Kurtakov <akurtako@redhat.com> 1.4-1
- Initial package.
