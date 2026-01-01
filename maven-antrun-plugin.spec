Name:           maven-antrun-plugin
Version:        3.1.0
Release:        1
Summary:        Maven AntRun Plugin
License:        Apache-2.0
URL:            https://maven.apache.org/plugins/maven-antrun-plugin/
BuildArch:      noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildRequires:  javapackages-bootstrap

%description
This plugin provides the ability to run Ant tasks from within Maven.
It is even possible to embed Ant scripts in the POM.

%prep
%autosetup -p1 -C

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE
