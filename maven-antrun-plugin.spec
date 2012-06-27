Name:           maven-antrun-plugin
Version:        1.7
Release:        2
Summary:        Maven AntRun Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-antrun-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip 
Patch0:         fix-deps.patch

BuildArch: noarch

BuildRequires: java-devel >= 1.6.0
BuildRequires: plexus-utils
BuildRequires: ant
BuildRequires: maven
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
Requires: ant
Requires: maven
Requires: jpackage-utils
Requires: java

Obsoletes: maven2-plugin-antrun <= 0:2.0.8
Provides: maven2-plugin-antrun = 1:%{version}-%{release}

%description
Runs Ant scripts embedded in the POM

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires: jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0
#%patch1

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%files
%doc LICENSE NOTICE
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

