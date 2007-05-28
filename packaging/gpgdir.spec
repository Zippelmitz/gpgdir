%define name gpgdir
%define version 1.2
%define release 1
%define gpgdirlibdir %_libdir/%name

### get the first @INC directory that includes the string "linux".
### This may be 'i386-linux', or 'i686-linux-thread-multi', etc.
%define gpgdirmoddir `perl -e '$path='i386-linux'; for (@INC) { if($_ =~ m|.*/(.*linux.*)|) {$path = $1; last; }} print $path'`

Summary: Gpgdir recursively encrypts/decrypts directories with GnuPG.
Name: %name
Version: %version
Release: %release
License: GPL
Group: Applications/Cryptography
Url: http://www.cipherdyne.org/gpgdir/
Source: %name-%version.tar.gz
BuildRoot: %_tmppath/%{name}-buildroot
#Prereq: rpm-helper

%description
gpgdir is a perl script that uses the CPAN GnuPG::Interface perl module to encrypt
and decrypt directories using a gpg key specified in ~/.gpgdirrc. gpgdir recursively
descends through a directory in order to make sure it encrypts or decrypts every file
in a directory and all of its subdirectories. By default the mtime and atime values
of all files will be preserved upon encryption and decryption (this can be disabled
with the --no-preserve-times option). Note that in --encrypt mode, gpgdir will
delete the original files that it successfully encrypts (unless the --no-delete
option is given). However, upon startup gpgdir first asks for a the decryption pass-
word to be sure that a dummy file can successfully be encrypted and decrypted. The
initial test can be disabled with the --skip-test option so that a directory can eas-
ily be encrypted without having to also specify a password (this is consistent with
gpg behavior). Also, note that gpgdir is careful not encrypt hidden files and direc-
tories. After all, you probably don't want your ~/.gnupg directory or ~/.bashrc file
to be encrypted.

%prep
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%setup -q
for i in $(grep -r "use lib" . | cut -d: -f1); do
    awk '/use lib/ { sub("/usr/lib/gpgdir", "%_libdir/%name") } { print }' $i > $i.tmp
    mv $i.tmp $i
done

cd Class-MethodMaker && perl Makefile.PL PREFIX=%gpgdirlibdir LIB=%gpgdirlibdir
cd ..
cd GnuPG-Interface && perl Makefile.PL PREFIX=%gpgdirlibdir LIB=%gpgdirlibdir
cd ..
cd TermReadKey && perl Makefile.PL PREFIX=%gpgdirlibdir LIB=%gpgdirlibdir
cd ..

%build
### build perl modules used by gpgdir
make OPTS="$RPM_OPT_FLAGS" -C Class-MethodMaker
make OPTS="$RPM_OPT_FLAGS" -C GnuPG-Interface
make OPTS="$RPM_OPT_FLAGS" -C TermReadKey

%install
### gpgdir module dirs
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Term/ReadKey
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/array
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/Engine
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/hash
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/scalar
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/Class/MethodMaker
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/Term
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/auto/GnuPG/Interface
mkdir -p $RPM_BUILD_ROOT%gpgdirlibdir/GnuPG
mkdir -p $RPM_BUILD_ROOT%_bindir
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%_sbindir

install -m 755 gpgdir $RPM_BUILD_ROOT%_bindir/
install -m 644 gpgdir.1 $RPM_BUILD_ROOT%{_mandir}/man1/

### install perl modules used by gpgdir
install -m 444 Class-MethodMaker/blib/lib/auto/Class/MethodMaker/array/*.* $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/array/
install -m 444 Class-MethodMaker/blib/lib/auto/Class/MethodMaker/scalar/*.* $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/scalar/
install -m 444 Class-MethodMaker/blib/lib/auto/Class/MethodMaker/hash/*.* $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/hash/
install -m 444 Class-MethodMaker/blib/lib/auto/Class/MethodMaker/Engine/*.* $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/Engine/
install -m 444 Class-MethodMaker/blib/arch/auto/Class/MethodMaker/MethodMaker.bs $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/MethodMaker.bs
install -m 444 Class-MethodMaker/blib/arch/auto/Class/MethodMaker/MethodMaker.so $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Class/MethodMaker/MethodMaker.so
install -m 444 Class-MethodMaker/blib/lib/Class/MethodMaker.pm $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/Class/MethodMaker.pm
install -m 444 Class-MethodMaker/blib/lib/Class/MethodMaker/*.pm $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/Class/MethodMaker
install -m 444 GnuPG-Interface/blib/lib/auto/GnuPG/Interface/*.* $RPM_BUILD_ROOT%gpgdirlibdir/auto/GnuPG/Interface/
install -m 444 GnuPG-Interface/blib/lib/GnuPG/*.pm $RPM_BUILD_ROOT%gpgdirlibdir/GnuPG/
install -m 444 TermReadKey/blib/lib/Term/ReadKey.pm $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/Term/ReadKey.pm
install -m 444 TermReadKey/blib/lib/auto/Term/ReadKey/autosplit.ix $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Term/ReadKey/autosplit.ix
install -m 444 TermReadKey/blib/arch/auto/Term/ReadKey/ReadKey.bs $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Term/ReadKey/ReadKey.bs
install -m 444 TermReadKey/blib/arch/auto/Term/ReadKey/ReadKey.so $RPM_BUILD_ROOT%gpgdirlibdir/%gpgdirmoddir/auto/Term/ReadKey/ReadKey.so

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%files
%defattr(-,root,root)
%_bindir/*
%{_mandir}/man1/*
%_libdir/%name

%changelog
* Mon May 28 2007 Michael Rash <mbr@cipherdyne.org>
- gpgdir-1.2 release

* Mon May 21 2007 Michael Rash <mbr@cipherdyne.org>
- gpgdir-1.1 release

* Sun Sep 17 2006 Michael Rash <mbr@cipherdyne.org>
- gpgdir-1.0.3 release (1.0.2 was skipped accidentally).

* Sat Sep 16 2006 Michael Rash <mbr@cipherdyne.org>
- Added x86_64 RPM.
- Removed iptables as a prerequisite.
- gpgdir-1.0.1 release

* Wed Sep 13 2006 Michael Rash <mbr@cipherdyne.org>
- gpgdir-1.0 release

* Thu Sep 09 2006 Michael Rash <mbr@cipherdyne.org>
- Initial RPM release of gpgdir-0.9.9
