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

%define gcj_support 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define _without_maven 1
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section free

Name:           directory-naming
Version:        0.8
Release:        %mkrel 2.0.1
Epoch:          0
Summary:        Directory Naming
License:        Apache Software License 2.0
Source0:        directory-naming-0.8.tar.gz
# svn export -r 124846 http://svn.apache.org/repos/asf/directory/sandbox/dormant-subprojects/naming/ directory-naming-0.8

Source1:        pom-maven2jpp-depcat.xsl
Source2:        pom-maven2jpp-newdepmap.xsl
Source3:        pom-maven2jpp-mapdeps.xsl
Source4:        directory-naming-0.8-jpp-depmap.xml
Source5:        http://repo1.maven.org/maven2/directory-naming/naming-core/0.8/naming-core-0.8.pom
Source6:        http://repo1.maven.org/maven2/directory-naming/naming-config/0.8/naming-config-0.8.pom
Source7:        http://repo1.maven.org/maven2/directory-naming/naming-factory/0.8/naming-factory-0.8.pom
Source8:        http://repo1.maven.org/maven2/directory-naming/naming-java/0.8/naming-java-0.8.pom
Source9:        http://repo1.maven.org/maven2/directory-naming/naming-management/0.8/naming-management-0.8.pom
Source10:       http://repo1.maven.org/maven2/directory-naming/naming-resources/0.8/naming-resources-0.8.pom

Patch0:         directory-naming-0.8-project.patch

URL:            http://directory.apache.org
Group:          Development/Java
BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  java-rpmbuild
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-nodeps
BuildRequires:  ant-junit
BuildRequires:  hsqldb
BuildRequires:  junit
%if %{with_maven}
BuildRequires:  maven >= 0:1.1
BuildRequires:  maven-plugins-base
BuildRequires:  maven-plugin-license
BuildRequires:  maven-plugin-multiproject
BuildRequires:  maven-plugin-test
BuildRequires:  maven-plugin-site
BuildRequires:  maven-plugin-xdoc
BuildRequires:  saxon
BuildRequires:  saxon-scripts
%endif
BuildRequires:  jakarta-commons-beanutils
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-dbcp
BuildRequires:  jakarta-commons-digester
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  jakarta-commons-pool
BuildRequires:  geronimo-javamail-1.3.1-api
BuildRequires:  mx4j

Requires:  jakarta-commons-beanutils
Requires:  jakarta-commons-collections
Requires:  jakarta-commons-dbcp
Requires:  jakarta-commons-digester
Requires:  jakarta-commons-lang
Requires:  jakarta-commons-logging
Requires:  jakarta-commons-pool
Requires:  geronimo-javamail-1.3.1-api
Requires:  mx4j
Requires(post):    jpackage-utils >= 0:1.7.3
Requires(postun):  jpackage-utils >= 0:1.7.3

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
Old directory/naming module.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%if %{with_maven}
%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
%{summary}.
%endif

%prep
%setup -q 
%remove_java_binaries
%patch0 -b .sav0

%build
%if %{with_maven}
if [ ! -f %{SOURCE4} ]; then
export DEPCAT=$(pwd)/directory-naming-0.8-depcat.new.xml
echo '<?xml version="1.0" standalone="yes"?>' > $DEPCAT
echo '<depset>' >> $DEPCAT
for p in $(find . -name project.xml); do
    pushd $(dirname $p)
    /usr/bin/saxon project.xml %{SOURCE1} >> $DEPCAT
    popd
done
echo >> $DEPCAT
echo '</depset>' >> $DEPCAT
/usr/bin/saxon $DEPCAT %{SOURCE2} > directory-naming-0.8-depmap.new.xml
fi

for p in $(find . -name project.xml); do
    pushd $(dirname $p)
    cp project.xml project.xml.orig
    /usr/bin/saxon -o project.xml project.xml.orig %{SOURCE3} map=%{SOURCE4}
    popd
done

export MAVEN_HOME_LOCAL=$(pwd)/.maven

maven \
        -Dmaven.repo.remote=file:/usr/share/maven/repository \
        -Dmaven.home.local=${MAVEN_HOME_LOCAL} \
        -Dgoal=jar:jar,javadoc:generate,xdoc:transform \
        multiproject:install multiproject:site
%else
export CLASSPATH=$(build-classpath \
commons-beanutils \
commons-collections \
commons-dbcp \
commons-digester \
commons-lang \
commons-logging \
commons-pool \
geronimo-javamail-1.3.1-api \
hsqldb \
junit \
mx4j/mx4j-jmx \
)
CLASSPATH=$CLASSPATH:$(pwd)/naming-core/target/naming-core-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/naming-java/target/naming-java-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/naming-resources/target/naming-resources-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/naming-management/target/naming-management-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/naming-factory/target/naming-factory-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
export OPT_JAR_LIST="ant/ant-nodeps ant/ant-junit junit"
%ant -Dbuild.sysclasspath=first jar javadoc
%endif

%install
rm -rf %{buildroot}
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

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
%__cp -pr target/docs/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%__rm -rf target/docs/apidocs

%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}/config
%__cp -pr target/docs/naming-config/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/config
%__rm -rf target/docs/naming-config/apidocs

%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}/core
%__cp -pr target/docs/naming-core/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/core
%__rm -rf target/docs/naming-core/apidocs

%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}/factory
%__cp -pr target/docs/naming-factory/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/factory
%__rm -rf target/docs/naming-factory/apidocs

%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}/java
%__cp -pr target/docs/naming-java/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/java
%__rm -rf target/docs/naming-java/apidocs

%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}/management
%__cp -pr target/docs/naming-management/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/management
%__rm -rf target/docs/naming-management/apidocs

%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}/resources
%__cp -pr target/docs/naming-resources/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/resources
%__rm -rf target/docs/naming-resources/apidocs
%else
%__cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
%endif

ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} 

# manual
%__mkdir_p %{buildroot}%{_docdir}/%{name}-%{version}
%__cp LICENSE.txt  %{buildroot}%{_docdir}/%{name}-%{version}
%if %{with_maven}
%__cp -pr target/docs/* %{buildroot}%{_docdir}/%{name}-%{version}
%endif

%{gcj_compile}

%clean
%__rm -rf %{buildroot}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}/LICENSE.txt 
%{_javadir}/%{name}
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%if %{with_maven}
%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}
%endif
