%define pyver 26
%define pybasever 2.6
%define unicode ucs4
%define autoconf autoconf2.6x
%define _default_patch_fuzz 2

%define python python%{pybasever}
%define tkinter tkinter%{pybasever}


%define demo_dir %{_libdir}/python%{pybasever}/Demo
%define tools_dir %{_libdir}/python%{pybasever}/Tools
%define doc_tools_dir %{_libdir}/python%{pybasever}/Doc/tools


Summary: An interpreted, interactive, object-oriented programming language
Name: python%{pyver}
Version: 2.6.4
Release: 1.ius.parallel%{?dist}
License: Python
Group: Development/Languages
Vendor: Rackspace US, Inc.
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}
Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

Patch0: Python-2.6.2-rhconfig.patch
Patch1: Python-2.2.1-pydocnogui.patch
Patch3: python-2.6.2-canonicalize.patch
Patch4: python-2.5-cflags.patch
Patch6: python-2.5.1-plural-fix.patch
Patch7: python-2.5.1-sqlite-encoding.patch
#Patch10: python-2.5.2-binutils-no-dep.patch
Patch11: python-2.5.1-codec-ascii-tolower.patch
Patch13: python-2.5.1-socketmodule-constants.patch
Patch14: python-2.5.1-socketmodule-constants2.patch
Patch16: python-2.6-rpath.patch

# Fix distutils to follow the Fedora/RHEL/CentOS policies of having .pyo files
Patch51: python-2.6-distutils_rpm.patch

# upstreamed

#Patch50: python-2.5-disable-egginfo.patch

# new db version
#Patch60: python-2.5.2-db47.patch

# lib64 patches
Patch101: python-2.3.4-lib64-regex.patch
Patch102: python-2.6-lib64.patch

# New API from 2.6

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: readline-devel, openssl-devel, gmp-devel
BuildRequires: ncurses-devel, gdbm-devel, zlib-devel, expat-devel
BuildRequires: libGL-devel tk tix gcc-c++ libX11-devel glibc-devel
BuildRequires: bzip2 tar /usr/bin/find pkgconfig tcl-devel tk-devel
BuildRequires: tix-devel bzip2-devel sqlite-devel
BuildRequires: autoconf26x
BuildRequires: db4-devel >= 4.3

URL: http://www.python.org/

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface. This package contains most of the standard
Python modules, as well as modules for interfacing to the Tix widget
set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Provides: libpython2.6.so.1.0
# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to 
use python as an embedded scripting language.  The python-libs package 
provides the libraries needed for this.

%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: %{python} < %{version}-%{release}

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: tkinter%{pyver} = %{version}-%{release}

%description tools
The Python package includes several development tools that are used
to build python programs.

%package -n tkinter%{pyver}
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
BuildRequires:  tcl, tk
Requires: %{name} = %{version}-%{release}
Requires: tk tix

%description -n tkinter%{pyver}

The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description test

The test modules from the main python pacakge: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you're developing python
code that uses more than just unittest and/or test_support.py.


%prep
%setup -q -n Python-%{version}
touch debugfiles.list

%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .no_gui
#%%patch2 -p1 -b .no-doc
%patch3 -p1 -b .canonicalize
%patch4 -p1 -b .cflags
#%%patch5 -p1 -b .ctypesexec
%patch6 -p1 -b .plural
%patch7 -p1
#%%patch8 -p1 -b .xmlrpc

# Try not disabling egg-infos, bz#414711
#patch50 -p1 -b .egginfo
#%%patch60 -p1 -b .db47

%if "%{_lib}" == "lib64"
%patch101 -p1 -b .lib64-regex
%patch102 -p1 -b .lib64
%endif

%patch11 -p1 -b .ascii-tolower
#%%patch12 -p1 -b .pysqlite-2.3.3-minimal
%patch13 -p1 -b .socketmodule
%patch14 -p1 -b .socketmodule2
#%%patch15 -p1 -b .listdir
%patch16 -p1 -b .rpath

%patch51 -p1 -b .brprpm

%ifarch alpha ia64
# 64bit, but not lib64 arches need this too...
%patch101 -p1 -b .lib64-regex
%endif

#%%patch260 -p1 -b .set_wakeup_fd

#%%patch999 -p1 -b .cve2007-4965
#%%patch998 -p0 -b .cve2008-2316

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f

%build
topdir=`pwd`
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export LINKCC="gcc"
if pkg-config openssl ; then
  export CFLAGS="$CFLAGS `pkg-config --cflags openssl`"
  export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi
# Force CC
export CC=gcc
# For patch 4, need to get a newer configure generated out of configure.in
%{autoconf}
%configure --enable-ipv6 --enable-unicode=%{unicode} --enable-shared --with-system-ffi

make OPT="$CFLAGS" %{?_smp_mflags}
LD_LIBRARY_PATH=$topdir $topdir/python Tools/scripts/pathfix.py -i "%{_bindir}/env python%{pybasever}" .
# Rebuild with new python
# We need a link to a versioned python in the build directory
ln -s python python%{pybasever}
LD_LIBRARY_PATH=$topdir PATH=$PATH:$topdir make -s OPT="$CFLAGS" %{?_smp_mflags}



%install
[ -d %{buildroot} ] && rm -fr %{buildroot}
mkdir -p %{buildroot}/usr %{buildroot}%{_mandir}

# Clean up patched .py files that are saved as .lib64
for f in distutils/command/install distutils/sysconfig; do
    rm -f Lib/$f.py.lib64
done

mkdir -p %{buildroot}
make altinstall DESTDIR=%{buildroot}

# Fix the interpreter path in binaries installed by distutils 
# (which changes them by itself)
# Make sure we preserve the file permissions
for fixed in %{buildroot}%{_bindir}/pydoc; do
    sed 's,#!.*/python$,#!%{_bindir}/env python%{pybasever},' $fixed > $fixed- \
        && cat $fixed- > $fixed && rm -f $fixed-
done

# Junk, no point in putting in -test sub-pkg
rm -f %{buildroot}/%{_libdir}/python%{pybasever}/idlelib/testcode.py*

# don't include tests that are run at build time in the package
# This is documented, and used: rhbz#387401
if /bin/false; then
 # Move this to -test subpackage.
mkdir save_bits_of_test
for i in test_support.py __init__.py; do
  cp -a %{buildroot}/%{_libdir}/python%{pybasever}/test/$i save_bits_of_test
done
rm -rf %{buildroot}/%{_libdir}/python%{pybasever}/test
mkdir %{buildroot}/%{_libdir}/python%{pybasever}/test
cp -a save_bits_of_test/* %{buildroot}/%{_libdir}/python%{pybasever}/test
fi


# tools

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/python%{pybasever}/site-packages

#modulator
cat > ${RPM_BUILD_ROOT}%{_bindir}/modulator << EOF
#!/bin/bash
exec %{_libdir}/python%{pybasever}/site-packages/modulator/modulator.py
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/modulator
cp -r Tools/modulator \
  ${RPM_BUILD_ROOT}%{_libdir}/python%{pybasever}/site-packages/

#pynche
cat > ${RPM_BUILD_ROOT}%{_bindir}/pynche << EOF
#!/bin/bash
exec %{_libdir}/python%{pybasever}/site-packages/pynche/pynche
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/pynche
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche \
  ${RPM_BUILD_ROOT}%{_libdir}/python%{pybasever}/site-packages/

mv Tools/modulator/README Tools/modulator/README.modulator
mv Tools/pynche/README Tools/pynche/README.pynche

#gettext
install -m755  Tools/i18n/pygettext.py %{buildroot}%{_bindir}/
install -m755  Tools/i18n/msgfmt.py %{buildroot}%{_bindir}/

# Useful development tools
install -m755 -d %{buildroot}%{tools_dir}/scripts
install Tools/README %{buildroot}%{tools_dir}/
install Tools/scripts/*py %{buildroot}%{tools_dir}/scripts/

# Documentation tools
install -m755 -d %{buildroot}%{doc_tools_dir}
#install -m755 Doc/tools/mkhowto %{buildroot}%{doc_tools_dir}

# Useful demo scripts
install -m755 -d %{buildroot}%{demo_dir}
cp -ar Demo/* %{buildroot}%{demo_dir}

# Get rid of crap
find %{buildroot}/ -name "*~"|xargs rm -f
find %{buildroot}/ -name ".cvsignore"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
#zero length
rm -f %{buildroot}%{_libdir}/python%{pybasever}/site-packages/modulator/Templates/copyright

rm -f %{buildroot}%{_libdir}/python%{pybasever}/LICENSE.txt


find %{buildroot}%{_libdir}/python%{pybasever}/lib-dynload -type d | sed "s|%{buildroot}|%dir |" > dynfiles
find %{buildroot}%{_libdir}/python%{pybasever}/lib-dynload -type f | \
  grep -v "_tkinter.so$" | \
  grep -v "_ctypes_test.so$" | \
  grep -v "_testcapimodule.so$" | \
  sed "s|%{buildroot}||" >> dynfiles


# Fix for bug #136654
rm -f %{buildroot}%{_libdir}/python%{pybasever}/email/test/data/audiotest.au %{buildroot}%{_libdir}/python%{pybasever}/test/audiotest.au

# Fix bug #143667: python should own /usr/lib/python2.x on 64-bit machines
%if "%{_lib}" == "lib64"
install -d %{buildroot}/usr/lib/python%{pybasever}/site-packages
%endif

# Make python-devel multilib-ready (bug #192747, #139911)
%define _pyconfig32_h pyconfig-32.h
%define _pyconfig64_h pyconfig-64.h

%ifarch ppc64 s390x x86_64 ia64 alpha sparc64
%define _pyconfig_h %{_pyconfig64_h}
%else
%define _pyconfig_h %{_pyconfig32_h}
%endif
mv %{buildroot}%{_includedir}/python%{pybasever}/pyconfig.h \
   %{buildroot}%{_includedir}/python%{pybasever}/%{_pyconfig_h}
cat > %{buildroot}%{_includedir}/python%{pybasever}/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
ln -s ../../libpython%{pybasever}.so %{buildroot}%{_libdir}/python%{pybasever}/config/libpython%{pybasever}.so

# Fix for bug 201434: make sure distutils looks at the right pyconfig.h file
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" %{buildroot}%{_libdir}/python%{pybasever}/distutils/sysconfig.py

# Get rid of egg-info files (core python modules are installed through rpms)
rm %{buildroot}%{_libdir}/python%{pybasever}/*.egg-info

# python's build is stupid and doesn't fail if extensions fail to build
# let's list a few that we care about...
for so in _bsddb.so _ctypes.so _cursesmodule.so _elementtree.so _sqlite3.so _ssl.so readline.so _hashlib.so zlibmodule.so bz2.so pyexpat.so; do
    if [ ! -f %{buildroot}/%{_libdir}/python%{pybasever}/lib-dynload/$so ]; then
       echo "Missing $so!!!"
       exit 1
    fi
done

# tag on the python version to bin files
mv %{buildroot}%{_bindir}/pydoc %{buildroot}%{_bindir}/pydoc%{pybasever}
mv %{buildroot}%{_bindir}/2to3 %{buildroot}%{_bindir}/2to3-%{pybasever}
mv %{buildroot}%{_bindir}/idle %{buildroot}%{_bindir}/idle%{pybasever}
mv %{buildroot}%{_bindir}/modulator %{buildroot}%{_bindir}/modulator%{pybasever}
mv %{buildroot}%{_bindir}/msgfmt.py %{buildroot}%{_bindir}/msgfmt%{pybasever}.py
mv %{buildroot}%{_bindir}/pygettext.py %{buildroot}%{_bindir}/pygettext%{pybasever}.py
mv %{buildroot}%{_bindir}/pynche %{buildroot}%{_bindir}/pynche%{pybasever}
mv %{buildroot}%{_bindir}/smtpd.py %{buildroot}%{_bindir}/smtpd%{pybasever}.py


%clean
rm -fr %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -f dynfiles
%defattr(-, root, root)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python*
%{_bindir}/python%{pybasever}

%dir %{_libdir}/python%{pybasever}
%dir %{_libdir}/python%{pybasever}/site-packages
%{_libdir}/python%{pybasever}/site-packages/README
%{_libdir}/python%{pybasever}/*.py*
%{_libdir}/python%{pybasever}/*.doc
%dir %{_libdir}/python%{pybasever}/bsddb
%{_libdir}/python%{pybasever}/bsddb/*.py*
%{_libdir}/python%{pybasever}/compiler
%dir %{_libdir}/python%{pybasever}/ctypes
%{_libdir}/python%{pybasever}/ctypes/*.py*
%{_libdir}/python%{pybasever}/ctypes/macholib
%{_libdir}/python%{pybasever}/curses
%dir %{_libdir}/python%{pybasever}/distutils
%{_libdir}/python%{pybasever}/distutils/*.py*
%{_libdir}/python%{pybasever}/distutils/README
%{_libdir}/python%{pybasever}/distutils/command
%dir %{_libdir}/python%{pybasever}/email
%{_libdir}/python%{pybasever}/email/*.py*
%{_libdir}/python%{pybasever}/email/mime
%{_libdir}/python%{pybasever}/encodings
%{_libdir}/python%{pybasever}/hotshot
%{_libdir}/python%{pybasever}/idlelib
%dir %{_libdir}/python%{pybasever}/json
%{_libdir}/python%{pybasever}/json/*.py*
%{_libdir}/python%{pybasever}/logging
%{_libdir}/python%{pybasever}/multiprocessing
%{_libdir}/python%{pybasever}/plat-linux2
%dir %{_libdir}/python%{pybasever}/sqlite3
%{_libdir}/python%{pybasever}/sqlite3/*.py*
%dir %{_libdir}/python%{pybasever}/test
%{_libdir}/python%{pybasever}/test/test_support.py*
%{_libdir}/python%{pybasever}/test/__init__.py*
%{_libdir}/python%{pybasever}/wsgiref*
%{_libdir}/python%{pybasever}/xml
%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%endif

%files libs
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/libpython%{pybasever}.so.*

%files devel
%defattr(-,root,root)
%{_prefix}/include/*
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%dir %{_libdir}/python%{pybasever}/config
%{_libdir}/python%{pybasever}/config/*
%{_libdir}/libpython%{pybasever}.so

%files tools
%defattr(-,root,root,755)
%doc Tools/modulator/README.modulator
%doc Tools/pynche/README.pynche
%{_libdir}/python%{pybasever}/lib2to3
%{_libdir}/python%{pybasever}/site-packages/modulator
%{_libdir}/python%{pybasever}/site-packages/pynche
%{_bindir}/smtpd*.py*
%{_bindir}/2to3*
%{_bindir}/idle*
%{_bindir}/modulator*
%{_bindir}/pynche*
%{_bindir}/pygettext*.py*
%{_bindir}/msgfmt*.py*
%{tools_dir}
%{demo_dir}

%files -n tkinter%{pyver}
%defattr(-,root,root,755)
%{_libdir}/python%{pybasever}/lib-tk
%{_libdir}/python%{pybasever}/lib-dynload/_tkinter.so

%files test
%defattr(-, root, root)
%{_libdir}/python%{pybasever}/bsddb/test
%{_libdir}/python%{pybasever}/ctypes/test
%{_libdir}/python%{pybasever}/distutils/tests
%{_libdir}/python%{pybasever}/email/test
%{_libdir}/python%{pybasever}/json/tests
%{_libdir}/python%{pybasever}/sqlite3/test
%{_libdir}/python%{pybasever}/test
%{_libdir}/python%{pybasever}/lib-dynload/_ctypes_test.so
%{_libdir}/python%{pybasever}/lib-dynload/_testcapimodule.so

%changelog
* Sun Nov 08 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6.4-1.ius.parallel
- Latest sources from upstream.
- Adding .parallel designates this package is a parallel install, not replacement
- BuildRequires: autoconf26x
- Removed Patch200: python-2.6-autoconf.patch

* Tue Sep 01 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6.2-1.ius
- Latest sources from upstream.
- Replaced Patch0: python-2.6-config.patch with
  Patch0: Python-2.6.2-rhconfig.patch
- Replaced Patch3: python-2.6-canonicalize.patch with
  Patch3: python-2.6.2-canonicalize.patch
- Replaced Patch200: python-2.6-autoconf.patch with
  Patch200: Python-2.6.2-autoconf.patch
- Removed Patch10: python-2.5.2-binutils-no-dep.patch
- Build with system ffi
- Add -lcrypt to crypto module

* Tue Aug 18 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.6.ius
- python26-libs provides libpython2.6.so.1.0 

* Thu Jul 23 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.5.ius
- Repackaging for IUS

* Tue May 19 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.5.rs
- Use side-by-side rather than installing to /opt/rackspace
- Removed Patch201: python26-2.6-opt_rackspace.patch

* Thu May 14 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.4.rs
- Added Patch201: python26-2.6-opt_rackspace.patch

* Tue Mar 24 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.3.rs
- Remove /usr from /opt/rackspace prefix.
- Moved tk files under tkinter package so that python26 does not
  require tix/tk any longer.

* Fri Mar 20 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.2.rs
- Requires: rs-optconfig

* Mon Mar 09 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.6-4.1.rs
- Rebuild 
- Adding Patch200: python-2.6-autoconf.patch

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.6-4
- rebuild with new openssl

* Tue Jan  6 2009 James Antill <james.antill@redhat.com> - 2.6-3
- Fix distutils generated rpms.
- Resolves: bug#236535

* Wed Dec 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.6-2
- Enable -lcrypt for cryptmodule

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.6-1
- Update to 2.6

* Tue Sep 30 2008 James Antill <james.antill@redhat.com> - 2.5.2-1
- Move to 2.5.2
- Fix CVE-2008-2316 hashlib overflow.

* Thu Jul 17 2008 Jeremy Katz <katzj@redhat.com> - 2.5.1-30
- Fix up the build for new rpm
- And actually build against db4-4.7 (#455170)

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-27
- fix license tag
- enable support for db4-4.7

* Sun Jun 15 2008 James Antill <jantill@redhat.com> - 2.5.1-26
- Fix sporadic listdir problem
- Resolves: bug#451494

* Mon Apr  7 2008 James Antill <jantill@redhat.com> - 2.5.1-25
- Rebuild to re-gen autoconf file due to glibc change.
- Resolves: bug#441003

* Tue Mar 25 2008 James Antill <jantill@redhat.com> - 2.5.1-24
- Add more constants to socketmodule

* Sat Mar  8 2008 James Antill <jantill@redhat.com> - 2.5.1-22
- Add constants to socketmodule
- Resolves: bug#436560

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.1-22
- Autorebuild for GCC 4.3

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-21
- rebuild for new tk in rawhide

* Mon Jan  7 2008 James Antill <jantill@redhat.com> - 2.5.1-20
- Add valgrind support files, as doc, to python-devel
- Relates: rhbz#418621
- Add new API from 2.6, set_wakeup_fd ... use at own risk, presumably won't
- change but I have no control to guarantee that.
- Resolves: rhbz#427794
- Add gdbinit support file, as doc, to python-devel

* Fri Jan  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-19
- rebuild for new tcl/tk in rawhide

* Fri Dec  7 2007 James Antill <jantill@redhat.com> - 2.5.1-18
- Create a python-test sub-module, over 3MB of stuff noone wants.
- Don't remove egginfo files, try this see what happens ... may revert.
- Resolves: rhbz#414711

* Mon Dec  3 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-17
- rebuild for new libssl

* Fri Nov 30 2007 James Antill <jantill@redhat.com> - 2.5.1-16
- Fix pyconfig.h comment typo.
- Add back test_support.py and the __init__.py file.
- Resolves: rhbz#387401

* Tue Oct 30 2007 James Antill <jantill@redhat.com> - 2.5.1-15
- Do codec lowercase in C Locale.
- Resolves: 207134 191096
- Fix stupid namespacing in pysqlite, minimal upgrade to 2.3.3 pysqlite
- Resolves: 263221

* Wed Oct 24 2007 James Antill <jantill@redhat.com> - 2.5.1-14
- Remove bintuils dep. for live CD ... add work around for ctypes

* Mon Oct 22 2007 James Antill <jantill@redhat.com> - 2.5.1-13
- Add tix buildprereq
- Add tkinter patch
- Resolves: #281751
- Fix ctypes loading of libraries, add requires on binutils
- Resolves: #307221
- Possible fix for CVE-2007-4965 possible exploitable integer overflow
- Resolves: #295971

* Tue Oct 16 2007 Mike Bonnet <mikeb@redhat.com> - 2.5.1-12
- fix marshalling of objects in xmlrpclib (python bug #1739842)

* Fri Sep 14 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-11
- fix encoding of sqlite .py files to work around weird encoding problem 
  in Turkish (#283331)

* Mon Sep 10 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-10
- work around problems with multi-line plural specification (#252136)

* Tue Aug 28 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-9
- rebuild against new expat

* Tue Aug 14 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-8
- build against db4.6

* Tue Aug 14 2007 Dennis Gilmore <dennis@ausil.us> - 2.5.1-7
- add sparc64 to the list of archs for _pyconfig64_h

* Fri Aug 10 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-6
- fix ctypes again on some arches (Hans de Goede, #251637)

* Fri Jul  6 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-5
- link curses modules with ncursesw (#246385)

* Wed Jun 27 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-4
- fix _elementtree.so build (#245703)
- ensure that extension modules we expect are actually built rather than 
  having them silently fall out of the package

* Tue Jun 26 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-3
- link with system expat (#245703)

* Thu Jun 21 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-2
- rebuild to take advantage of hardlinking between identical pyc/pyo files

* Thu May 31 2007 Jeremy Katz <katzj@redhat.com> - 2.5.1-1
- update to python 2.5.1

* Mon Mar 19 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-12
- fix alpha build (#231961)

* Tue Feb 13 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-11
- tcl/tk was reverted; rebuild again

* Thu Feb  1 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-10
- rebuild for new tcl/tk

* Tue Jan 16 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.5.3-9
- link with ncurses

* Sat Jan  6 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-8
- fix extensions to use shared libpython (#219564)
- all 64bit platforms need the regex fix (#122304)

* Wed Jan  3 2007 Jeremy Katz <katzj@redhat.com> - 2.5.3-7
- fix ctypes to not require execstack (#220669)

* Fri Dec 15 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-6
- don't link against compat-db (Robert Scheck)

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> - 2.5.3-5
- fix invalid assert in debug mode (upstream changeset 52622)

* Tue Dec 12 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-4
- obsolete/provide python-ctypes (#219256)

* Mon Dec 11 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-3
- fix atexit traceback with failed syslog logger (#218214)
- split libpython into python-libs subpackage for multilib apps 
  embedding python interpreters

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.5.3-2
- disable installation of .egg-info files for now

* Tue Dec  5 2006 Jeremy Katz <katzj@redhat.com>
- support db 4.5
- obsolete python-elementtree; since it requires some code tweaks, don't 
  provide it
- obsolete old python-sqlite; provide the version that's actually included

* Mon Oct 30 2006 Jeremy Katz <katzj@redhat.com>
- fix _md5 and _sha modules (Robert Sheck)
- no longer provide optik compat; it's been a couple of years now
- no longer provide the old shm module; if this is still needed, let's 
  build it separately
- no longer provide japanese codecs; should be a separate package

* Mon Oct 23 2006 Jeremy Katz <katzj@redhat.com> - 2.5-0
- update to 2.5.0 final

* Fri Aug 18 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.99.c1
- Updated to 2.5c1. Merged fixes from FC6 too:
- Fixed bug #199373 (on some platforms CFLAGS is needed when linking)
- Fixed bug #198971 (case conversion not locale safe in logging library)
- Verified bug #201434 (distutils.sysconfig is confused by the change to make
  python-devel multilib friendly) is fixed upstream

* Sun Jul 16 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.99.b2
- Updated to 2.5b2 (which for comparison reasons is re-labeled 2.4.99.b2)

* Fri Jun 23 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.99.b1
- Updated to 2.5b1 (which for comparison reasons is re-labeled 2.4.99.b1)

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-11.FC6
- and fix it for real

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-10.FC6
- fix python-devel on ia64

* Tue Jun 13 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-9
- Fixed python-devel to be multilib friendly (bug #192747, #139911)

* Tue Jun 13 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-8
- Only copying mkhowto from the Docs - we don't need perl dependencies from
  python-tools.

* Mon Jun 12 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-7
- Fixed bug #121198 (webbrowser.py should use the user's preferences first)

* Mon Jun 12 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-6
- Fixed bug #192592 (too aggressive assertion fails) - SF#1257960
- Fixed bug #167468 (Doc/tools not included) - added in the python-tools package

* Thu Jun  8 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-5
- Fixed bug #193484 (added pydoc in the main package)

* Mon Jun  5 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-4
- Added dist in the release

* Mon May 15 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-3
- rebuilt to fix broken libX11 dependency

* Wed Apr 12 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-2
- rebuild with new gcc to fix #188649

* Thu Apr  6 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-1
- Updated to 2.4.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-3.2.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-3.2
- rebuilt for newer tix

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Mihai Ibanescu <misa@redhat.com> 2.4.2-3
- fixed #136654 for another instance of audiotest.au

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 19 2005 Bill Nottingham <notting@redhat.com> 2.4.2-2
- fix build for modular X, remove X11R6 path references

* Tue Nov 15 2005 Mihai Ibanescu <misa@redhat.com> 2.4.2-1
- Upgraded to 2.4.2
- BuildRequires autoconf

* Wed Nov  9 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-16
- Rebuilding against newer openssl.
- XFree86-devel no longer exists

* Mon Sep 26 2005 Peter Jones <pjones@redhat.com> 2.4.1-14
- Once more -- this time, to fix -EPERM when you run it in a directory
  you can't read from.

* Mon Sep 26 2005 Peter Jones <pjones@redhat.com> 2.4.1-13
- So, 5 or 6 people have said it works for them with this patch...

* Sun Sep 25 2005 Peter Jones <pjones@redhat.com> 2.4.1-12
- Fixed bug #169159 (check for argc>0 and argv[0] == NULL, not just
    argv[0][0]='\0')
  Reworked the patch from -8 a bit more.

* Fri Sep 23 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-10
- Fixed bug #169159 (don't let python core dump if no arguments are passed in)
  Reworked the patch from -8 a bit more.

* Thu Sep 22 2005 Peter Jones <pjones@redhat.com> 2.4.1-8
- Fix bug #169046 more correctly.

* Thu Sep 22 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-7
- Fixed bug #169046 (realpath is unsafe); thanks to 
  Peter Jones <pjones@redhat.com> and Arjan van de Ven <arjanv@redhat.com> for
  diagnosing and the patch.

* Tue Sep 20 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-4
- Fixed bug #168655 (fixes for building as python24)

* Tue Jul 26 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-3
- Fixed bug #163435 (pynche doesn't start))

* Wed Apr 20 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-2
- Fixed bug #143667 (python should own /usr/lib/python* on 64-bit systems, for
  noarch packages)
- Fixed bug #143419 (BuildRequires db4 is not versioned)

* Wed Apr  6 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-1
- updated to 2.4.1

* Mon Mar 14 2005 Mihai Ibanescu <misa@redhat.com> 2.4-6
- building the docs from a different source rpm, to decouple bootstrapping
  python from having tetex installed

* Fri Mar 11 2005 Dan Williams <dcbw@redhat.com> 2.4-5
- Rebuild to pick up new libssl.so.5

* Wed Feb  2 2005 Mihai Ibanescu <misa@redhat.com> 2.4-4
- Fixed security issue in SimpleXMLRPCServer.py (#146647)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.4-3
- Rebuilt for new readline.

* Mon Dec  6 2004 Jeff Johnson <jbj@jbj.org> 2.4-2
- db-4.3.21 returns DB_BUFFER_SMALL rather than ENOMEM (#141994).
- add Provide: python(abi) = 2.4
- include msgfmt/pygettext *.pyc and *.pyo from brp-python-bytecompile.

* Fri Dec  3 2004 Mihai Ibanescu <misa@redhat.com> 2.4-1
- Python-2.4.tar.bz2 (final)

* Fri Nov 19 2004 Mihai Ibanescu <misa@redhat.com> 2.4-0.c1.1
- Python-2.4c1.tar.bz2 (release candidate 1)

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2.4-0.b2.4
- rebuild against db-4.3.21.

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.4-0.b2.3
- fix the lib64 patch so that 64bit arches still look in /usr/lib/python...

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.4-0.b2.2
- cryptmodule still needs -lcrypt (again)

* Thu Nov  4 2004 Mihai Ibanescu <misa@redhat.com> 2.4-0.b2.1
- Updated to python 2.4b2 (and labeled it 2.4-0.b2.1 to avoid breaking rpm's
  version comparison)

* Thu Nov  4 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-13
- Fixed bug #138112 (python overflows stack buffer) - SF bug 105470

* Tue Nov  2 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-12
- Fixed bugs #131439 #136023 #137863 (.pyc/.pyo files had the buildroot added)

* Tue Oct 26 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-11
- Fixed bug #136654 (python has sketchy audio clip)

* Tue Aug 31 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-10
- Fixed bug #77418 (Demo dir not packaged)
- More tweaking on #19347 (Moved Tools/ under /usr/lib/python2.3/Tools)

* Fri Aug 13 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-8
- Fixed bug #129769: Makefile in new python conflicts with older version found
  in old python-devel
- Reorganized the spec file to get rid of the aspython2 define; pybasever
  is more powerful.

* Tue Aug  3 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-7
- Including html documentation for non-i386 arches
- Fixed #125362 (python-doc html files have japanese character encoding)
- Fixed #128923 (missing dependency between python and python-devel)

* Fri Jul 30 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-6
- Fixed #128030 (help() not printing anything)
- Fixed #125472 (distutils.sysconfig.get_python_lib() not returning the right
  path on 64-bit systems)
- Fixed #127357 (building python as a shared library)
- Fixed  #19347 (including the contents of Tools/scripts/ in python-tools)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-3
- Added an optik.py that provides the same interface from optparse for
  backward compatibility; obsoleting python-optik

* Mon Jun  7 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-2
- Patched bdist_rpm to allow for builds of multiple binary rpms (bug #123598)

* Fri Jun  4 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-1
- Updated to 2.3.4-1 with Robert Scheck's help (bug #124764)
- Added BuildRequires: tix-devel (bug #124918)

* Fri May  7 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-6
- Correct fix for #122304 from upstream:
  http://sourceforge.net/tracker/?func=detail&atid=105470&aid=931848&group_id=5470

* Thu May  6 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-4
- Fix for bug #122304 : splitting the domain name fails on 64-bit arches
- Fix for bug #120879 : including Makefile into the main package

- Requires XFree86-devel instead of -libs (see bug #118442)

* Tue Mar 16 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-3
- Requires XFree86-devel instead of -libs (see bug #118442)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec 19 2003 Jeff Johnson <jbj@jbj.org> 2.3.3-1
- upgrade to 2.3.3.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 2.3.2-9
- rebuild against db-4.2.52.

* Fri Dec 12 2003 Jeremy Katz <katzj@redhat.com> 2.3.2-8
- more rebuilding for new tcl/tk

* Wed Dec  3 2003 Jeff Johnson <jbj@jbj.org> 2.3.2-7.1
- rebuild against db-4.2.42.

* Fri Nov 28 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-7
- rebuilt against newer tcl/tk

* Mon Nov 24 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-6
- added a Provides: python-abi

* Wed Nov 12 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-5
- force CC (#109268)

* Sun Nov  9 2003 Jeremy Katz <katzj@redhat.com> 2.3.2-4
- cryptmodule still needs -lcrypt

* Wed Nov  5 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-2
- Added patch for missing mkhowto

* Thu Oct 16 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-1
- Updated to 2.3.2

* Thu Sep 25 2003 Mihai Ibanescu <misa@redhat.com> 2.3.1-1
- 2.3.1 final

* Tue Sep 23 2003 Mihai Ibanescu <misa@redhat.com> 2.3.1-0.8.RC1
- Building the python 2.3.1 release candidate
- Updated the lib64 patch

* Wed Jul 30 2003 Mihai Ibanescu <misa@redhat.com> 2.3-0.2
- Building python 2.3
- Added more BuildRequires
- Updated the startup files for modulator and pynche; idle installs its own
  now.

* Thu Jul  3 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-4
- Rebuilt against newer db4 packages (bug #98539)

* Mon Jun 9 2003 Elliot Lee <sopwith@redhat.com> 2.2.3-3
- rebuilt

* Wed Jun  7 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-2
- Rebuilt

* Tue Jun  6 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-1
- Upgraded to 2.2.3

* Wed Apr  2 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-28
- Rebuilt

* Wed Apr  2 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-27
- Modified the ftpuri patch conforming to http://ietf.org/rfc/rfc1738.txt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-25
- Fixed bug #84886: pydoc dies when run w/o arguments
- Fixed bug #84205: add python shm module back (used to be shipped with 1.5.2)
- Fixed bug #84966: path in byte-compiled code still wrong

* Thu Feb 20 2003 Jeremy Katz <katzj@redhat.com> 2.2.2-23
- ftp uri's should be able to specify being rooted at the root instead of 
  where you login via ftp (#84692)

* Mon Feb 10 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-22
- Using newer Japanese codecs (1.4.9). Thanks to 
  Peter Bowen <pzb@datastacks.com> for pointing this out.

* Thu Feb  6 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-21
- Rebuild

* Wed Feb  5 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-20
- Release number bumped really high: turning on UCS4 (ABI compatibility
  breakage)

* Fri Jan 31 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-13
- Attempt to look both in /usr/lib64 and /usr/lib/python2.2/site-packages/:
  some work on python-2.2.2-lib64.patch

* Thu Jan 30 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-12
- Rebuild to incorporate the removal of .lib64 and - files.

* Thu Jan 30 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-11.7.3
- Fixed bug #82544: Errata removes most tools
- Fixed bug #82435: Python 2.2.2 errata breaks redhat-config-users
- Removed .lib64 and - files that get installed after we fix the multilib
  .py files.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 2.2.2-10
- rebuild to update tkinter's tcltk deps
- convert changelog to utf-8

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.2-9
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- pick up OpenSSL cflags and ldflags from pkgconfig if available

* Thu Jan  2 2003 Jeremy Katz <katzj@redhat.com> 2.2.2-8
- urllib2 didn't support non-anonymous ftp.  add support based on how 
  urllib did it (#80676, #78168)

* Mon Dec 16 2002 Mihai Ibanescu <misa@redhat.com> 2.2.2-7
- Fix bug #79647 (Rebuild of SRPM fails if python isn't installed)
- Added a bunch of missing BuildRequires found while fixing the
  above-mentioned bug

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 2.2.2-6
- rebuild to fix broken tcltk deps for tkinter

* Fri Nov 22 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-3.7.3
- Recompiled for 7.3 (to fix the -lcrypt bug)
- Fix for the spurious error message at the end of the build (build-requires
  gets confused by executable files starting with """"): make the tests
  non-executable.

* Wed Nov 20 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-5
- Fixed configuration patch to add -lcrypt when compiling cryptmodule.c

2.2.2-4
- Spec file change from Matt Wilson <msw@redhat.com> to disable linking 
  with the C++ compiler.

* Mon Nov 11 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-3.*
- Merged patch from Karsten Hopp <karsten@redhat.de> from 2.2.1-17hammer to
  use %%{_libdir}
- Added XFree86-libs as BuildRequires (because of tkinter)
- Fixed duplicate listing of plat-linux2
- Fixed exclusion of lib-dynload/japanese
- Added lib64 patch for the japanese codecs
- Use setup magic instead of using tar directly on JapaneseCodecs

* Tue Nov  5 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-2
- Fix #76912 (python-tools contains idle, which uses tkinter, but there is no
  requirement of tkinter from python-tools).
- Fix #74013 (rpm is missing the /usr/lib/python2.2/test directory)

* Mon Nov  4 2002 Mihai Ibanescu <misa@redhat.com>
- builds as python2 require a different libdb
- changed the buildroot name of python to match python2 builds

* Fri Nov  1 2002 Mihai Ibanescu <misa@redhat.com>
- updated python to 2.2.2 and adjusted the patches accordingly

* Mon Oct 21 2002 Mihai Ibanescu <misa@redhat.com>
- Fix #53930 (Python-2.2.1-buildroot-bytecode.patch)
- Added BuildPrereq dependency on gcc-c++

* Fri Aug 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-17
- security fix for _execvpe

* Tue Aug 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-16
- Fix  #71011,#71134, #58157

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-15
- Resurrect tkinter
- Fix for distutils (#67671)
- Fix #69962

* Thu Jul 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-14
- Obsolete tkinter/tkinter2 (#69838)

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-13
- Doc fixes (#53951) - not on alpha at the momemt

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-12
- fix pydoc (#68082)

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-11
- Add db4-devel as a BuildPrereq

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.2.1-10
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-9
- Add Japanese codecs (#66352)

* Tue Jun 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-8
- No more tkinter...

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-7
- Rebuild

* Tue May 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-6
- Add the email subcomponent (#65301)

* Fri May 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-5
- Rebuild

* Thu May 02 2002 Than Ngo <than@redhat.com> 2.2.1-4
- rebuild i new enviroment

* Tue Apr 23 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Use ucs2, not ucs4, to avoid breaking tkinter (#63965)

* Mon Apr 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-2
- Make it use db4

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-1
- 2.2.1 - a bugfix-only release

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-16
- the same, but in builddirs - this will remove them from the 
  docs package, which doesn't look in the buildroot for files.

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-15
- Get rid of temporary files and .cvsignores included 
  in the tarball and make install

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-14
- Don't own lib-tk in main package, only in tkinter (#62753)

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-13
- rebuild

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-12
- rebuild

* Fri Mar  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-11
- Add a not to the Distutils obsoletes test (doh!)

* Fri Mar  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-10
- Rebuild

* Mon Feb 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-9
- Only obsolete Distutils when built as python

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-8
- Make files in /usr/bin install side by side with python 1.5 when
- Drop explicit requirement of db4
  built as python2

* Thu Jan 31 2002 Elliot Lee <sopwith@redhat.com> 2.2-7
- Use version and pybasever macros to make updating easy
- Use _smp_mflags macro

* Tue Jan 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-6
- Add db4-devel to BuildPrereq

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.2-5
- disable ndbm support, which is db2 in disguise (really interesting things
  can happen when you mix db2 and db4 in a single application)

* Thu Jan 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-4
- Obsolete subpackages if necesarry 
- provide versioned python2
- build with db4

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-3
- Alpha toolchain broken. Disable build on alpha.
- New openssl

* Wed Dec 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-1
- 2.2 final

* Fri Dec 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.11c1
- 2.2 RC 1
- Don't include the _tkinter module in the main package - it's 
  already in the tkiter packace
- Turn off the mpzmodule, something broke in the buildroot

* Wed Nov 28 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.10b2
- Use -fPIC for OPT as well, in lack of a proper libpython.so

* Mon Nov 26 2001 Matt Wilson <msw@redhat.com> 2.2-0.9b2
- changed DESTDIR to point to / so that distutils will install dynload
  modules properly in the installroot

* Fri Nov 16 2001 Matt Wilson <msw@redhat.com> 2.2-0.8b2
- 2.2b2

* Fri Oct 26 2001 Matt Wilson <msw@redhat.com> 2.2-0.7b1
- python2ify

* Fri Oct 19 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.5b1
- 2.2b1

* Sun Sep 30 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.4a4
- 2.2a4
- Enable UCS4 support
- Enable IPv6
- Provide distutils
- Include msgfmt.py and pygettext.py

* Fri Sep 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.3a3
- Obsolete Distutils, which is now part of the main package
- Obsolete python2

* Thu Sep 13 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.2a3
- Add docs, tools and tkinter subpackages, to match the 1.5 layout

* Wed Sep 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.1a3
- 2.2a3
- don't build tix and blt extensions

* Mon Aug 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add tk and tix to build dependencies

* Sat Jul 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.1 bugfix release - with a GPL compatible license

* Fri Jul 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add new build dependencies (#49753)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- build with -fPIC

* Fri Jun  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1
- reorganization of file includes

* Wed Dec 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the "requires" clause, it lacked a space causing problems
- use %%{_tmppath}
- don't define name, version etc
- add the available patches from the Python home page

* Fri Dec 15 2000 Matt Wilson <msw@redhat.com>
- added devel subpackage

* Fri Dec 15 2000 Matt Wilson <msw@redhat.com>
- modify all files to use "python2.0" as the intrepter
- don't build the Expat bindings
- build against db1

* Mon Oct 16 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for 2.0 final

* Mon Oct  9 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for 2.0c1
- build audioop, imageop, and rgbimg extension modules
- include xml.parsers subpackage
- add test.xml.out to files list

* Thu Oct  5 2000 Jeremy Hylton <jeremy@beopen.com>
- added bin/python2.0 to files list (suggested by Martin v. L?)

* Tue Sep 26 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for release 1 of 2.0b2
- use .bz2 version of Python source

* Tue Sep 12 2000 Jeremy Hylton <jeremy@beopen.com>
- Version 2 of 2.0b1
- Make the package relocatable.  Thanks to Suchandra Thapa.
- Exclude Tkinter from main RPM.  If it is in a separate RPM, it is
  easier to track Tk releases.
