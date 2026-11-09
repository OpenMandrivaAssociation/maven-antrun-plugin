Name:		maven-antrun-plugin
Version:	3.2.0
Release:	1
Summary:	Runs Ant tasks from a Maven build
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/plugins/maven-antrun-plugin/
Source0:	https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
# Modello is not packaged. This jar is source. Only the generated
# taskconfig classes are copied out of it.
Source1:	%{name}-%{version}-sources.jar
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
# Generates META-INF/maven/plugin.xml. The separate annotations package
# conflicts with maven-components on the same index file.
BuildRequires:	maven-plugin-tools
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	mvn(org.apache.ant:ant)
BuildRequires:	ant-lib >= 1.10.18
Requires:	ant-lib >= 1.10.18
# plexus-xml is not packaged. ReaderFactory is not in plexus-utils
# 3.6.2; XmlStreamReader is.
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven2-plugin-antrun <= 0:2.0.8
Provides:	maven2-plugin-antrun = %{EVRD}
Obsoletes:	maven-antrun-plugin-javadoc < %{EVRD}

%description
Runs Ant tasks embedded in a POM. 3.2.0 is the current stable release.
Modello is not packaged, so the generated task configuration classes
come from the upstream sources jar. Tests need JUnit Jupiter and
XMLUnit, so they are not run.

%prep
%autosetup -n %{name}-%{version}
rm -rf src/test src/it .github
python - <<'PY'
import zipfile
from pathlib import Path

dest = Path("src/main/java/org/apache/maven/plugins/antrun/taskconfig")
dest.mkdir(parents=True)
wanted = (
    "org/apache/maven/plugins/antrun/taskconfig/AttachArtifactConfiguration.java",
    "org/apache/maven/plugins/antrun/taskconfig/DependencyFilesetsConfiguration.java",
)
with zipfile.ZipFile("%{SOURCE1}") as archive:
    for name in wanted:
        (dest / Path(name).name).write_bytes(archive.read(name))
path = Path("src/main/java/org/apache/maven/plugins/antrun/AntRunMojo.java")
text = path.read_text(encoding="utf-8")
text = text.replace(
    "import org.codehaus.plexus.util.ReaderFactory;\n",
    "import org.codehaus.plexus.util.xml.XmlStreamReader;\n",
)
text = text.replace("ReaderFactory.newXmlReader(", "new XmlStreamReader(")
path.write_text(text, encoding="utf-8")
PY
python - <<'PY'
import xml.etree.ElementTree as ET

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.plugins")
add(root, "artifactId", "maven-antrun-plugin")
add(root, "version", "%{version}")
add(root, "packaging", "maven-plugin")
add(root, "name", "Apache Maven AntRun Plugin")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
items = (
    ("org.apache.ant", "ant", "1.10.18", None),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", None),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-artifact", "3.10.0", "provided"),
    ("org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3", "provided"),
    ("javax.inject", "javax.inject", "1", "provided"),
    ("org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided"),
)
for group, artifact, version, scope in items:
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
build = ET.SubElement(root, tag("build"))
plugins = ET.SubElement(build, tag("plugins"))
plugin = ET.SubElement(plugins, tag("plugin"))
add(plugin, "groupId", "org.apache.maven.plugins")
add(plugin, "artifactId", "maven-plugin-plugin")
add(plugin, "version", "3.16.0")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE NOTICE
