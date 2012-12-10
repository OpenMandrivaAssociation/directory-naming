# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           directory-naming
Version:        0.8
Release:        6
Summary:        Apache Directory Naming Component
License:        ASL 2.0
URL:            http://directory.apache.org
Group:          Development/Java

Source0:        directory-naming-0.8.tar.bz2
# svn export -r 124846 http://svn.apache.org/repos/asf/directory/sandbox/dormant-subprojects/naming/ directory-naming-0.8

Source5:        http://repo1.maven.org/maven2/directory-naming/naming-core/0.8/naming-core-0.8.pom
Source6:        http://repo1.maven.org/maven2/directory-naming/naming-config/0.8/naming-config-0.8.pom
Source7:        http://repo1.maven.org/maven2/directory-naming/naming-factory/0.8/naming-factory-0.8.pom
Source8:        http://repo1.maven.org/maven2/directory-naming/naming-java/0.8/naming-java-0.8.pom
Source9:        http://repo1.maven.org/maven2/directory-naming/naming-management/0.8/naming-management-0.8.pom
Source10:       http://repo1.maven.org/maven2/directory-naming/naming-resources/0.8/naming-resources-0.8.pom

BuildRequires:  jpackage-utils >= 1.7.3
BuildRequires:  java-devel >= 1.4.2
BuildRequires:  ant >= 1.6.5
BuildRequires:  hsqldb
BuildRequires:  junit
BuildRequires:  ant-junit
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-dbcp
BuildRequires:  jakarta-commons-digester
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  jakarta-commons-pool
BuildRequires:  classpathx-mail
BuildRequires:  mx4j

Requires:  jakarta-commons-beanutils
Requires:  jakarta-commons-collections
Requires:  jakarta-commons-dbcp
Requires:  jakarta-commons-digester
Requires:  jakarta-commons-lang
Requires:  jakarta-commons-logging
Requires:  jakarta-commons-pool
Requires:  classpathx-mail
Requires:  mx4j
Requires(post):    jpackage-utils >= 1.7.3
Requires(postun):  jpackage-utils >= 1.7.3

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Naming is a lightweight, in-memory JNDI service provider.  To
enable flexible deployment with limited dependencies, Naming is divided in 6
packages, each producing a separate jar artifact.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q
# remove all binary libs
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done
sed -i "s/\r//" LICENSE.txt

%build
export CLASSPATH=$(build-classpath \
commons-beanutils \
commons-collections \
commons-dbcp \
commons-digester \
commons-lang \
commons-logging \
commons-pool \
hsqldb \
javamail \
junit \
mx4j/mx4j-jmx \
)

CLASSPATH=$CLASSPATH:$(pwd)/naming-config/target/classes:$(pwd)/naming-config/target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/naming-core/target/classes:$(pwd)/naming-core/target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/naming-factory/target/classes:$(pwd)/naming-factory/target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/naming-java/target/classes:$(pwd)/naming-java/target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/naming-management/target/classes:$(pwd)/naming-management/target/test-classes
CLASSPATH=$CLASSPATH:$(pwd)/naming-resources/target/classes:$(pwd)/naming-resources/target/test-classes

export OPT_JAR_LIST="junit ant/ant-junit"

ant -Dbuild.sysclasspath=only jar javadoc

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true
# jars
%__mkdir_p %{buildroot}%{_javadir}/%{name}
for p in \
         naming-config \
         naming-core \
         naming-factory \
         naming-java \
         naming-management \
         naming-resources \
         ; do
%__install -m 644 $p/target/$p-%{version}.jar %{buildroot}%{_javadir}/%{name}/$p-%{version}.jar
done
(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*; do %__ln_s ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# poms
%__mkdir_p %{buildroot}%{_datadir}/maven2/poms
%__install -m 644 %{SOURCE5}  %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-naming-core.pom
%add_to_maven_depmap %{name} naming-core %{version} JPP/%{name} naming-core
%__install -m 644 %{SOURCE6}  %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-naming-config.pom
%add_to_maven_depmap %{name} naming-config %{version} JPP/%{name} naming-config
%__install -m 644 %{SOURCE7}  %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-naming-factory.pom
%add_to_maven_depmap %{name} naming-factory %{version} JPP/%{name} naming-factory
%__install -m 644 %{SOURCE8}  %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-naming-java.pom
%add_to_maven_depmap %{name} naming-java %{version} JPP/%{name} naming-java
%__install -m 644 %{SOURCE9}  %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-naming-management.pom
%add_to_maven_depmap %{name} naming-management %{version} JPP/%{name} naming-management
%__install -m 644 %{SOURCE10} %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-naming-resources.pom
%add_to_maven_depmap %{name} naming-resources %{version} JPP/%{name} naming-resources

# docs
%__mkdir_p %{buildroot}%{_docdir}/%{name}-%{version}
%__cp LICENSE.txt  %{buildroot}%{_docdir}/%{name}-%{version}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%{_docdir}/*
%{_javadir}/%{name}
%{_datadir}/maven2/poms/*
%config %{_mavendepmapfragdir}



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 0.8-6
+ Revision: 733869
- rebuild
- imported package directory-naming

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.8-2.0.3mdv2011.0
+ Revision: 617785
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 0:0.8-2.0.2mdv2010.0
+ Revision: 428249
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0:0.8-2.0.1mdv2009.0
+ Revision: 266563
- rebuild early 2009.0 package (before pixel changes)

* Fri May 09 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.8-1.0.1mdv2009.0
+ Revision: 204975
- add ant-junit BR
- put ant-nodeps on the opt_jar_list
- BR ant-nodeps
- import directory-naming


