%{?_javapackages_macros:%_javapackages_macros}
Summary:        An open source data binding framework for Java
Name:           castor
Version:        1.3.2
Release:        10.1%{?dist}
Epoch:          0

License:        BSD and MPLv1.1 and W3C
URL:            https://castor.codehaus.org
Source0:        http://dist.codehaus.org/castor/%{version}/castor-%{version}-src.tgz
Patch0:         castor-fix-unmappable-chars.patch

BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-gpg-plugin
BuildRequires:  codehaus-parent
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-logging
BuildRequires:  regexp
BuildRequires:  ldapjdk
BuildRequires:  jakarta-oro
BuildRequires:  bea-stax
BuildRequires:  velocity
BuildRequires:  multithreadedtc
BuildRequires:  easymock3
BuildRequires:  mockito
BuildRequires:  javacc-maven-plugin
BuildRequires:  castor-maven-plugin
BuildRequires:  geronimo-jpa
BuildRequires:  geronimo-jta
Obsoletes:      castor-demo < 0:1.3.2
Obsoletes:      castor-test < 0:1.3.2
Obsoletes:      castor-xml < 0:1.3.2
Obsoletes:      castor-doc < 0:1.3.2

%description
Castor is an open source data binding framework for Java. It's basically
the shortest path between Java objects, XML documents and SQL tables.
Castor provides Java to XML binding, Java to SQL persistence, and more.

%package javadoc

Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%patch0

# Disable uneeded modules
%pom_disable_module anttask
%pom_disable_module xmlctf-framework
%pom_disable_module maven-plugins

# Disable integration test suites
%pom_disable_module cpactf
%pom_disable_module jpa-extensions-it
%pom_disable_module xmlctf

# Remove test deps that are not in Fedora
%pom_remove_dep tyrex:tyrex
%pom_remove_dep tyrex:tyrex cpa
%pom_xpath_remove "pom:build/pom:extensions"

# Fix dep on cglib
sed -i 's@cglib-nodep@cglib@g' pom.xml cpa/pom.xml

# Fix dep on mtc
sed -i 's@edu.umd.cs.mtc@edu.umd.cs@g' pom.xml xml/pom.xml

# Fix dep on ant
sed -i 's@groupId>ant<@groupId>org.apache.ant<@g' pom.xml xml/pom.xml

%build
%mvn_build -- -Dgpg.skip=true -Dmaven.test.skip=true

%install
%mvn_install

%files -f .mfiles
%doc src/doc/license.txt src/doc/new-license.txt

%files javadoc -f .mfiles-javadoc
%doc src/doc/license.txt src/doc/new-license.txt

%changelog
* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.3.2-10
- Add BR on castor-maven-pluing
- Perform non-bootstrap build

* Fri Aug 09 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.3.2-9
- Bootstrap XML modules with pre-generated source, this is needed to build
  castor-maven-plugin, which is needed to generate the source we are using
  to bootstrap

* Fri Aug 09 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.3.2-8
- Add missing BR, fixes FTBFS rhbz #992042
- Use pom macros instead of patching
- Install poms/depmaps and licence files

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.3.2-6
- Disable maven-wagon extension, fixes FTBFS rhbz #913914

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.3.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.2-1
- Update to latest upstream version.
- Most modules disabled hence all old subpackages are obsolete now.

* Wed Apr 20 2011 Alexander Kurtakov <akurtako@redhat.com> 0:0.9.5-7
- Update to current guidelines.
- Fix oro deps.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.5-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.5-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 08 2009 Karsten Hopp <karsten@redhat.com> 0.9.5-4.1
- Specify source and target as 1.4 to make it build

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.9.5-3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:0.9.5-2jpp.8
- Autorebuild for GCC 4.3

* Wed Apr 18 2007 Permaine Cheung <pcheung@redhat.com> - 0:0.9.5-1jpp.8
- Update spec file as per fedora review process.

* Thu Aug 03 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.9.5-1jpp.7
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:0.9.5-1jpp_6fc
- Rebuilt

* Thu Jul  20 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.9.5-1jpp_5fc
- Added conditional native compilation.
- Added missing BR/R for log4j.

* Thu Jun  8 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.9.5-1jpp_4fc
- Updated project URL -- fix for Bug #180586

* Wed Mar  8 2006 Rafael Schloming <rafaels@redhat.com> - 0:0.9.5-1jpp_3fc
- excluded s390[x] and ppc64 due to eclipse

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:0.9.5-1jpp_2fc
- stop scriptlet spew

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> 0:0.9.5-1jpp_1fc
- Build into Fedora.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles and classfiles from the tarball.

* Thu Jun  2 2005 Gary Benson <gbenson@redhat.com>
- Fix up (alleged) invalid characters in the documentation.

* Fri Jul 23 2004 Fernando Nasser <fnasser@redhat.com> 0:0.9.5-1jpp_3rh
- use servletapi5 instead of servletapi4

* Thu Mar 11 2004 Frank Ch. Eigler <fche@redhat.com> 0:0.9.5-1jpp_2rh
- try servletapi4 instead of servletapi3
- add example-servletapi4 patch

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 0:0.9.5-1jpp_1rh
- RH vacuuming

* Tue Sep 09 2003 David Walluck <david@anti-microsoft.org> 0:0.9.5-1jpp
- 0.9.5

* Fri May 16 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:0.9.4.3-2jpp
- use same lsapjdk package as tyrex

* Sat May 10 2003 David Walluck <david@anti-microsoft.org> 0:0.9.4.3-1jpp
- release
