Summary:        An open source data binding framework for Java
Name:           castor
Version:        1.3.2
Release:        1
Epoch:          0
Group:          Development/Java
License:        BSD and MPLv1.1 and W3C
URL:            http://castor.codehaus.org
Source0:        http://dist.codehaus.org/castor/1.3.2/castor-1.3.2-src.tgz
Patch0:         disable-modules.patch
BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  codehaus-parent
BuildRequires:  maven-enforcer-plugin
Requires:       apache-commons-logging
Requires:       apache-commons-lang
Obsoletes:      castor-demo < 0:1.3.2
Obsoletes:      castor-test < 0:1.3.2
Obsoletes:      castor-xml < 0:1.3.2
Obsoletes:      castor-doc < 0:1.3.2

%description
Castor is an open source data binding framework for Java. It's basically
the shortest path between Java objects, XML documents and SQL tables.
Castor provides Java to XML binding, Java to SQL persistence, and more.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;
%patch0 -p0 -b .sav

sed -i 's/Class-Path: xerces.jar jdbc-se2.0.jar jndi.jar jta1.0.1.jar//' src/etc/MANIFEST.MF

%build
mvn-rpmbuild -X -Dgpg.skip=true -Dmaven.test.skip=true install javadoc:aggregate

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 core/target/%{name}-core-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/%{name}

