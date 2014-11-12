#
# spec file for package tamago
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           tamago
BuildRequires:  emacs-x11
Requires:       emacs
# updated 2013-08-27
#Version:        4.0.6_20011017cvs
Version:        4.0.6_20041122cvs
Release:        7.1
#Version:        4.0.6+0.20041122cvs # this version string is wrong .

Url:            http://www.m17n.org/tamago
# Other useful, tamago related URLs:
#     http://emacs-20.ki.nu/tamago/
#     http://cgi18.plala.or.jp/~nyy/canna/
#     http://www.gcd.org/sengoku/boiling-egg/
#     ftp://ftp.ki.nu/pub/emcws/README.html  (obsoleted by tamago)
# Source: ftp://ftp.m17n.org/pub/tamago/tamago-4.0.6.tar.gz
# I think it is better to use the CVS version, it already contains Canna support
# without the need of patches:
# get the tamago CVS source with:
#    cvs -d :pserver:anonymous@cvs.m17n.org:/cvs/tamago co tamago
# and create the following tarball:
#Source0:        tamago-_{version}.tar.bz2

# 2013-08-27 - bkbin005@rinku.zaq.ne.jp
# imported source from http://packages.debian.org/wheezy/egg .
# Because upstream http://www.m17n.org/tamago was dead,
# and egg_4.0.6+0.20041122cvs-19.diff.gz was fixed bnc#836138 .
Source0:        http://ftp.de.debian.org/debian/pool/main/e/egg/egg_4.0.6+0.20041122cvs.orig.tar.gz
# egg-canna.el was deleted 2013-08-27 by bkbin005@rinku.zaq.ne.jp
#Source1:        http://cgi18.plala.or.jp/nyy/canna/egg-canna.el.bz2

# 2013-09-09 - bkbin005@rinku.zaq.ne.jp
# Source[234]'s URLs were dead, so I deleted URL .
#Source2:        http://www.gcd.org/sengoku/boiling-egg/boiling-egg.el.bz2
#Source3:        http://www.m17n.org/tamago/pdf/ISFST99.pdf.bz2
#Source4:        http://www.m17n.org/tamago/pdf/LC99.pdf.bz2
Source2:        boiling-egg.el.bz2
Source3:        ISFST99.pdf.bz2
Source4:        LC99.pdf.bz2

Source5:        suse-start.el
# imported from http://packages.debian.org/wheezy/egg .
Source6:        http://ftp.de.debian.org/debian/pool/main/e/egg/egg_4.0.6+0.20041122cvs-19.dsc
Patch0:         eggrc.patch
# imported from http://packages.debian.org/wheezy/egg .
#PATCH-FIX-UPSTREAM egg_4.0.6+0.20041122cvs-19.diff.gz bnc#836138 bkbin005@rinku.zaq.ne.jp
Patch1:         http://ftp.de.debian.org/debian/pool/main/e/egg/egg_4.0.6+0.20041122cvs-19.diff.gz
#PATCH-FIX-OPENSUSE tamago-fix-access-to-fwnn.patch bnc#836138 bkbin005@rinku.zaq.ne.jp
Patch2:         tamago-fix-access-to-fwnn.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Summary:        Multilingual input method for Emacs
License:        GPL-2.0+
Group:          System/I18n/Japanese

%description
Tamago offers a multilingual input environment for GNU Emacs (>= 20.5).
It is completely written in Emacs Lisp and can use the backends FreeWnn
(jserver, cserver, tserver), Wnn6, SJ3 Ver.2, and Canna.



Authors:
--------
    NIIBE Yutaka <gniibe@chroot.org>
    KATAYAMA Yoshio <kate@pfu.co.jp>
    TOMURA Satoru <tomura@etl.go.jp>
    

%prep
%setup -n egg-4.0.6+0.20041122cvs
%patch1 -p1
%patch0 -p1

cp -p $RPM_SOURCE_DIR/suse-start.el .
#cp -p $RPM_SOURCE_DIR/egg-canna.el.bz2 . # deleted 2013-08-27 .
cp -p $RPM_SOURCE_DIR/boiling-egg.el.bz2 .
cp -p $RPM_SOURCE_DIR/*.pdf.bz2 .
bunzip2 *.bz2
find -type d -name "CVS" | xargs rm -rfv

%patch2 -p1

%build
%define emacs_sitelisp_dir %{_datadir}/emacs/site-lisp
%define emacs_package_dir %{emacs_sitelisp_dir}/egg
./configure --prefix=/usr
make
for i in boiling-egg # egg-canna was deleted 2013-08-27
do
   emacs -batch -q -no-site-file -no-init-file -f batch-byte-compile $i.el
done

%install
if [ -n "%{?buildroot}" ] ; then
   [ %{buildroot} != "/" ] && rm -rf %{buildroot}
fi
mkdir -p $RPM_BUILD_ROOT%{emacs_sitelisp_dir}
make install prefix=$RPM_BUILD_ROOT/usr
for i in boiling-egg # egg-canna was deleted 2013-08-27 .
do
    install -m644 $i.{el,elc} $RPM_BUILD_ROOT%{emacs_sitelisp_dir}
done
{
  echo ";; %{emacs_sitelisp_dir}/suse-start-%{name}.el"
  echo ""
  echo "(add-to-list 'load-path \"%{emacs_package_dir}\")"
  echo ""
  cat suse-start.el
  echo ""
  echo ";; %{emacs_sitelisp_dir}/suse-start-%{name}.el ends here"
} > %{buildroot}%{emacs_sitelisp_dir}/suse-start-%{name}.el

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog* PROBLEMS README* TODO *.pdf doc/*
%{emacs_package_dir}
%config %{emacs_sitelisp_dir}/suse-start-%{name}.el
# egg-canna was deleted 2013-08-27 by bkbin005@rinku.zaq.ne.jp
#_{emacs_sitelisp_dir}/egg-canna.el
#_{emacs_sitelisp_dir}/egg-canna.elc
%{emacs_sitelisp_dir}/boiling-egg.el
%{emacs_sitelisp_dir}/boiling-egg.elc

%changelog
* Sun Oct 19 2014 crrodriguez@opensuse.org
- Remove xorg-x11-devel from BuildRequires, noarch package
  does not need X libraries around.
* Sun Jun  1 2014 jengelh@inai.de
- Drop unused build-time requirements on libpng, libtiff, libgif
* Sun Sep  8 2013 bkbin005@rinku.zaq.ne.jp
- Fix tamago.changes:
  Fixed comment style .
- Fix tamago.spec:
  * fix commented-out macros: were changed to "_" .
    Because rpmlint tells them warning messages .
  * Source[234]'s URLs were dead, so I deleted URL .
  * Changed egg_4.0.6+0.20041122cvs-19.diff.gz
    to patch from source .
  * I deleted Japanese EUC-JP encoding comments .
  * I added a comment why am I import sources from Debian .
    Because upstream http://www.m17n.org/tamago was dead .
- Fix tamago-fix-access-to-fwnn.patch .
  I forgot to change comm-accept-timeout from nil to 1000
  in egg-com.el .
  So insert it in tamago-fix-access-to-fwnn.patch .
- Fix Version: tag in tamago.spec .
  I changed version string to Debian format .
  But its string was wrong, then fixed to openSUSE format .
- Fix that tamago can not access to FreeWnn's jserver
  (bnc#836138) .
  * Update to egg_4.0.6_20041122cvs.orig.tar.gz:
  * Imported source from http://packages.debian.org/wheezy/egg .
    http://ftp.de.debian.org/debian/pool/main/e/egg/egg_4.0.6+0.20041122cvs-19.dsc
    http://ftp.de.debian.org/debian/pool/main/e/egg/egg_4.0.6+0.20041122cvs.orig.tar.gz
    http://ftp.de.debian.org/debian/pool/main/e/egg/egg_4.0.6+0.20041122cvs-19.diff.gz
    Because upstream http://www.m17n.org/tamago wad dead,
    and egg_4.0.6+0.20041122cvs-19.diff.gz was fixed bnc#836138 .
  * Deleted source
    http://cgi18.plala.or.jp/nyy/canna/egg-canna.el.bz2 .
    Because this program can not run on Emacs-24.3-4.3 .
  * Added tamago-fix-access-to-fwnn.patch .
    Deleted (make-local-hook) function .
    And defvaralias 'last-command-char 'last-command-event .
    Because their function and variable are deleted
    from Emacs-24.3 .
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Feb  6 2004 hmacht@suse.de
- building as non-root
* Tue May 20 2003 ro@suse.de
- remove CVS subdirs
* Wed Nov 13 2002 ro@suse.de
- use x-devel-packages
* Fri Feb  1 2002 ro@suse.de
- changed neededforbuild <libpng> to <libpng-devel-packages>
* Thu Nov 15 2001 mfabian@suse.de
- small fix to suse-start-tamago.el to make it work with Emacs 21
  again
* Fri Nov  9 2001 mfabian@suse.de
- add libjpeg libpng libtiff libungif to '# neededforbuild'
* Thu Oct 18 2001 mfabian@suse.de
- new package: tamago-4.0.6_20011017cvs
