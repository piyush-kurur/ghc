# RPM spec file for GHC
#
# Copyright [1998..1999] Manuel M. T. Chakravarty <chak@acm.org>
# Thanks to Zoltan Vorosbaranyi <vbzoli@vbzo.li> for help with earlier 
# versions. 
#
# This file is subject to the same free software license as GHC.

# Values for @version@ and @patchlevel@ are set by the `configure' script.  
# SNAP releases are CVS snapshots.  Official releases should replace SNAP by
# an appropriate release numbers (they are usually numbered starting from 1).

%define version    @version@
%define patchlevel @patchlevel@
%define release    SNAP
%define prefix     /usr

Summary: Glasgow Haskell Compilation system
Name: ghc
Version: %{version}
Release: %{release}
Copyright: BSD style w/o adv. clause
Group: Development/Languages
Source: http://haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.gz
URL: http://haskell.org/ghc/
BuildRoot: /var/tmp/ghc-%{version}-%{release}-root
Packager: Manuel M. T. Chakravarty <chak@is.tsukuba.ac.jp>
Provides: haskell

%description
The Glorious Glasgow Haskell Compilation System (GHC) is a robust,
fully-featured, optimising compiler for the functional programming
language Haskell 98.  GHC compiles Haskell to either native code or
C. It implements numerous experimental language extensions to Haskell,
including concurrency, a foreign language interface, several
type-system extensions, exceptions, and so on. GHC comes with a
generational garbage collector, a space and time profiler, and a
comprehensive set of libraries.  This package includes HTML and PS
versions of the SGML-based documentation for GHC.  They are also available 
online at http://www.haskell.org/ghc/.

Haskell 98 is "the" standard lazy functional programming language.
More info plus the language definition is at http://www.haskell.org/.

** This package does not include libraries for profiling **

%changelog

* Tue Dec 7 1999 Manuel Chakravarty
- version for use from CVS

* Thu Sep 16 1999 Manuel Chakravarty
- modified for GHC 4.04, patchlevel 1 (no more 62 tuple stuff); minimises use
  of patch files - instead emits a build.mk on-the-fly

* Sat Jul 31 1999 Manuel Chakravarty
- modified for GHC 4.04

* Wed Jun 30 1999 Manuel Chakravarty
- some more improvements from vbzoli

* Fri Feb 26 1999 Manuel Chakravarty
- modified for GHC 4.02

* Thu Dec 24 1998 Zoltan Vorosbaranyi 
- added BuildRoot
- files located in /usr/local/bin, /usr/local/lib moved to /usr/bin, /usr/lib

* Tue Jul 28 1998 Manuel Chakravarty
- original version

%prep
%setup -n fptools

# generate our own `build.mk'
#
# * this is a kludge, to be used until the `configure' script is improved
#
cat >mk/build.mk <<END
GhcHcOpts = -O -dcore-lint -H24m
GhcCompilerWays =
GhcLibWays = 
GhcLibHcOpts = -O -H24m -split-objs -odir \$* 
GhcLibsWithReadline = YES
StripLibraries = YES
SRC_HAPPY_OPTS += -c
END


%build
./configure --prefix=%{prefix} --libdir=%{prefix}/lib/ghc-%{version}
make boot
make -C glafp-utils sgmlverb
make all
make -C docs ps html
make -C ghc/docs/users_guide ps html
make -C ghc/docs/libraries ps html

%install
# compress the non-html docs
#
for j in docs ghc/docs; do
  dir=`pwd`
  cd $j
  for i in ps dvi sgml vsgml verb idx; do
    find . -name '*.'$i -exec gzip -9 '{}' ';' -print
  done
  cd $dir
done
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix}\
     libdir=$RPM_BUILD_ROOT%{prefix}/lib/ghc-%{version} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc ghc/ANNOUNCE ghc/PATCHLEVEL ghc/README docs/ ghc/docs/ CONTRIB/
%{prefix}/bin/ghc
%{prefix}/bin/ghc-%{version}
%{prefix}/bin/hp2ps
%{prefix}/bin/hstags
%{prefix}/bin/stat2resid
%{prefix}/lib/ghc-%{version}/
