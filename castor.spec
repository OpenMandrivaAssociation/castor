# FIXME:
# W: castor class-path-in-manifest /usr/share/java/castor-1.0.5.jar
# W: castor-xml class-path-in-manifest /usr/share/java/castor-xml-1.0.5.jar

%define gcj_support     1
# XXX: This requires org.mockebj.*
%bcond_with             examples
%bcond_with             tests

Summary:        An open source data binding framework for Java
Name:           castor
Version:        1.0.5
Release:        %mkrel 2
Epoch:          0
Group:          Development/Java
License:        BSD-style
URL:            http://www.castor.org/
Source0:        http://dist.codehaus.org/castor/%{version}/castor-%{version}-src.tgz
Patch0:         example-servletapi4.patch
Patch1:         example-servletapi5.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       adaptx
Requires:       cglib-nohook
Requires:       jakarta-commons-logging
Requires:       jdbc-stdext
Requires:       jndi
Requires:       jta
Requires:       ldapjdk
Requires:       log4j
Requires:       oro
Requires:       regexp
Requires:       xerces-j2
BuildRequires:  adaptx
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  cglib-nohook
BuildRequires:  xalan-j2
BuildRequires:  jakarta-commons-logging
BuildRequires:  jdbc-stdext
BuildRequires:  jndi
BuildRequires:  jpackage-utils >= 0:1.5.16
BuildRequires:  jta
BuildRequires:  ldapjdk
BuildRequires:  log4j
BuildRequires:  oro
BuildRequires:  regexp
BuildRequires:  xerces-j2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel >= 0:1.0.31
Requires(post):   java-gcj-compat >= 0:1.0.31
Requires(postun): java-gcj-compat >= 0:1.0.31
%else
BuildArch:        noarch
%endif

%description
Castor is an open source data binding framework for Java. It's basically
the shortest path between Java objects, XML documents and SQL tables.
Castor provides Java to XML binding, Java to SQL persistence, and then
some more.

%package demo
Group:          Development/Java
Summary:        Demo for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       servletapi5
BuildRequires:  servletapi5 

%description demo
Demonstrations and samples for %{name}.

%if %with tests
%package test
Group:          Development/Java
Summary:        Tests for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       junit
BuildRequires:  junit

%description test
Tests for %{name}.
%endif

%package xml
Group:          Development/Java
Summary:        XML support for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description xml
XML support for Castor.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package doc
Summary:        Documentation for %{name}
Group:          Development/Java

%description doc
Documentation for %{name}.

%prep
%setup -q
find . -type f -name "*.jar" | %{_bindir}/xargs -t %{__rm}
find . -type f -name "*.class" | %{_bindir}/xargs -t %{__rm}
%if 0
find . -name "*.java" -exec perl -p -i -e 's|assert\(|assertTrue\(|g;' {} \;
find . -name "*.java" -exec perl -p -i -e 's|_test.name\(\)|_test.getName\(\)|g;' {} \;
find src/doc -name "*.xml" -exec perl -p -i -e 's|\222|&#x92;|g;' {} \;
%endif
%patch0
%patch1

%build
export CLASSPATH=$(build-classpath adaptx cglib-nohook jakarta-commons-logging jdbc-stdext jndi jta junit ldapjdk log4j oro regexp servletapi5 xerces-j2)
export OPT_JAR_LIST="adaptx ant/ant-trax xalan-j2 xalan-j2-serializer"
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' src/build.xml
%{ant} -Dbuild.sysclasspath=only -buildfile src/build.xml jar
%if %with examples
%{ant} -buildfile src/build.xml compile.examples
%endif
%if %with tests
%{ant} -buildfile src/build.xml CTFjar
%endif
%{ant} -buildfile src/build.xml javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/%{name}-%{version}-xml.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xml-%{version}.jar
%if %with tests
install -m 644 dist/CTF-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tests-%{version}.jar
%endif
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}

%if %with examples
# examples (demo)
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/examples
cp -pr build/examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}/examples
%endif

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# do this last, since it will delete all build directories
export CLASSPATH=$(build-classpath adaptx cglib-nohook jakarta-commons-logging jdbc-stdext jndi jta junit ldapjdk log4j oro regexp servletapi5 xerces-j2)
export OPT_JAR_LIST="adaptx ant/ant-trax xalan-j2 xalan-j2-serializer"
%{ant} -buildfile src/build.xml doc

# like magic
%jpackage_script org.exolab.castor.builder.SourceGenerator %{nil} %{nil} xerces-j2:%{name} %{name}

%{__perl} -pi -e 's/\r$//g' src/etc/CHANGELOG \
                            src/main/resources/LICENSE \
                            src/main/resources/README \
                            build/doc/*.{css,dtd,txt} \
                            build/doc/**/*.htm \
                            build/doc/ora-mar-2k/*.htm

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc src/etc/CHANGELOG src/main/resources/LICENSE src/main/resources/README
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%dir %{_datadir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%if %with examples
%{_datadir}/%{name}/examples
%endif

%if %with tests
%files test
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-tests-%{version}.jar
%{_javadir}/%{name}-tests.jar
%endif

%files xml
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-xml-%{version}.jar
%{_javadir}/%{name}-xml.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files doc
%defattr(0644,root,root,0755)
%doc build/doc/*


