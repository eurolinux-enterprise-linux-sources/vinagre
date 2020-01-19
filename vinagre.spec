%ifarch %{ix86} x86_64
%define with_spice 1
%endif

Name:           vinagre
Version:        3.22.0
Release:        9%{?dist}
Summary:        VNC client for GNOME

Group:          Applications/System
License:        GPLv2+
URL:            https://wiki.gnome.org/Apps/Vinagre
#VCS: git:git://git.gnome.org/vinagre
Source0:        https://download.gnome.org/sources/%{name}/3.22/%{name}-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1376044
Patch0:         vinagre-3.14.3-RDP-update.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1384965
Patch1:         vinagre-3.22.0-freerdp-versions.patch
Patch2:         vinagre-3.22.0-rdp-connection-cancel.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1435715
Patch3:         vinagre-3.22.0-fullscreen-toolbar.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1459111
Patch4:         vinagre-3.22.0-share-clipboard.patch

%if 0%{?with_spice}
BuildRequires:  pkgconfig(spice-client-gtk-3.0)
%endif
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(avahi-ui-gtk3)
BuildRequires:  pkgconfig(freerdp)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-vnc-2.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(telepathy-glib)
BuildRequires:  pkgconfig(vte-2.91)
BuildRequires:  gnome-common
BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  vala-devel
BuildRequires:  libappstream-glib-devel
BuildRequires:  yelp-tools
BuildRequires:  autoconf
BuildRequires:  automake

# for /usr/share/dbus-1/services
Requires: dbus
Requires: telepathy-filesystem

%description
Vinagre is a VNC client for the GNOME desktop.

With Vinagre you can have several connections open simultaneously, bookmark
your servers thanks to the Favorites support, store the passwords in the
GNOME keyring, and browse the network to look for VNC servers.

Apart from the VNC protocol, vinagre supports Spice and RDP.


%prep
%setup -q
%patch0 -p1 -b .RDP-update
%patch1 -p1 -b .freerdp-versions
%patch2 -p1 -b .rdp-connection-cancel
%patch3 -p1 -b .fullscreen-toolbar
%patch4 -p1 -b .share-clipboard

%build
autoreconf -ivf
%configure \
%if 0%{?with_spice}
           --enable-spice \
%endif
           --enable-rdp \
           --enable-ssh \
           --with-avahi
make V=1 %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

%find_lang vinagre --with-gnome


%check
make check


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :


%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/mime/packages &>/dev/null || :
  update-mime-database -n %{_datadir}/mime &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database -n %{_datadir}/mime &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f vinagre.lang
%doc AUTHORS NEWS README
%license COPYING
%{_bindir}/vinagre
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/vinagre-mime.xml
%{_datadir}/vinagre/
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Vinagre.service
%{_datadir}/telepathy/clients/Vinagre.client
%{_datadir}/glib-2.0/schemas/org.gnome.Vinagre.gschema.xml
%dir %{_datadir}/GConf/
%dir %{_datadir}/GConf/gsettings/
%{_datadir}/GConf/gsettings/org.gnome.Vinagre.convert
%doc %{_mandir}/man1/vinagre.1.gz


%changelog
* Mon Sep 25 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-9
- Fix "Share clipboard" functionality in Spice plugin
- Resolves: #1459111

* Mon Mar 27 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-8
- Rebuild with new spice-gtk3
- Related: #1435715

* Fri Mar 24 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-7
- Fix showing of fullscreen toolbar
- Resolves: #1435715

* Wed Mar 15 2017 Kalev Lember <klember@redhat.com> - 3.22.0-6
- Rebuilt for spice-gtk3 soname bump
- Related: #1402474

* Thu Mar  2 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-5
- ifdef some variables based on FreeRDP version (Coverity)
- Related: #1384965

* Thu Mar  2 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-4
- Rebuild with newer shared-mime-info
- Related: #1384965

* Tue Feb 28 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-3
- Don't rely on file triggers (they need newer rpm)
- Related: #1384965

* Thu Feb 16 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-2
- Add patches
- Related: #1384965

* Wed Feb 15 2017 Marek Kasik <mkasik@redhat.com> - 3.22.0-1
- Update to 3.22.0
- Remove/modify current patches when needed
- Rely on file triggers
- Resolves: #1384965

* Mon Sep 19 2016 Marek Kasik <mkasik@redhat.com> - 3.14.3-11
- Handle connection failures of RDP plugin
- Resolves: #1375720

* Mon Sep 19 2016 Marek Kasik <mkasik@redhat.com> - 3.14.3-10
- Check RDP events in timeout GSource not in idle
- Resolves: #1376044

* Thu Sep 8 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-9
- Focus on new RDP tab
- Do not capture key events of other tabs
- Resolves: #1291275

* Tue Aug 30 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-8
- Allow to open multiple connections with same host
- Resolves: #1291275

* Thu May 05 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-7
- Correct authentication attempts control
- Add missing translations
- Resolves: #1291275

* Wed Apr 27 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-6
- Add minimize button to the fullscreen toolbar
- Handle domain when looking for credentials
- Store credentials for RDP
- Fix RDP initialization with recent FreeRDP
- Allow scalling of RDP sessions
- Resolves: #1291275

* Fri Mar 18 2016 Marek Kasik <mkasik@redhat.com> - 3.14.3-5
- Add missing translations (patch by Parag Nemade)
- Resolves: #1304230

* Tue Mar 01 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-4
- Use cached session size for RDP
- Resolves: #1291281

* Tue Mar 01 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-3
- Fix selection rectangle when user leaves window
- Resolves: #1291287

* Thu Feb 25 2016 Felipe Borges <feborges@redhat.com> - 3.14.3-2
- Change SPICE passwords limited to 60 characters
- Resolves: #1291297

* Thu Apr 30 2015 Marek Kasik <mkasik@redhat.com> - 3.14.3-1
- Update to 3.14.3
- Add translations update from translation team
- Add translation fix from upstream
- Remove unused patches
- Resolves: #1174568

* Mon Oct 20 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-12
- Add translations of new strings
- Resolves: #1142870

* Wed Sep 17 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-11
- Add build-dependency of yelp-tools
- Related: #1091765

* Wed Sep 17 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-10
- Run autoreconf because of modified configure.ac
- Related: #1091765

* Wed Sep 17 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-9
- Use FreeRDP API in RDP plugin
- Request RDP certificate verification if needed
- Add available translations for new strings
- Resolves: #1091765

* Wed Sep 17 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-8
- Allow to customize desktop size for RDP protocol
- Add available translations for new strings
- Resolves: #862389

* Tue Sep 16 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-7
- Show correct title in error dialog
- Resolves: #1141150

* Wed Sep 10 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-6
- Rebuild because of rpmdiff
- Related: #1068615

* Wed Sep 10 2014 Marek Kasik <mkasik@redhat.com> - 3.8.2-5
- Don't close connect dialog when showing help
- Resolves: #1068615

* Tue Jan 28 2014 David King <dking@redhat.com> - 3.8.2-4
- Fix storing passwords in libsecret (#1055914)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8.2-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.8.2-2
- Mass rebuild 2013-12-27

* Wed Jul  3 2013 Marek Kasik <mkasik@redhat.com> - 3.8.2-1.2
- Enable RDP again and switch to FreeRDP
- Resolves: #978825

* Thu Jun 27 2013 Marek Kasik <mkasik@redhat.com> - 3.8.2-1.1
- Disable RDP plugin temporarily
- Related: #978825

* Tue May 14 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Tue Apr 23 2013 Mat Booth <fedora@matbooth.co.uk> - 3.8.1-2
- Add explicit dep on rdesktop for RDP functionality (#903225)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Fri Mar  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Wed Sep 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Thu Sep  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.90-2
- Rebuild against new spice

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Thu Aug 09 2012 Christophe Fergeau <cfergeau@redhat.com> - 3.5.2-3
- Rebuilt against new spice-gtk

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Dropped upstreamed translation patch

* Wed Mar 28 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-2
- Fix the build by fixing the Russian help translation.

* Tue Mar 27 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Fri Mar  9 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.3.4-3
- Own %%{_datadir}/telepathy and %%{_datadir}/GConf dirs (#681636).

* Mon Feb 13 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-2
- Update the description to mention RDP and Spice

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.3.2-2
- Fix the spice plugin

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90
- Make the dbus dep archful

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Wed Aug 03 2011 Adam Williamson <awilliam@redhat.com> - 3.1.4-2
- rebuild against updated spice

* Mon Jul 25 2011 Matthew Barnes <mbarnes@redhat.com> 3.1.4-1
- Update to 3.1.4

* Tue Jul 05 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Mon Jun 20 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-3
- Fix vala sources compilation

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-2
- Fix the main notebook widget expansion

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Removed -devel package

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-3
- Update scriptlets

* Thu Apr 28 2011 Dan Horák <dan[at]danny.cz> - 3.0.1-2
- spice available only on x86

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Tue Apr  5 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-2
- Kill off the remnants of GConf, this uses GSettings now.
- Bring back ssh support (by building against vte3 instead of vte)

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-2
- Fix build

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Mar  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.8-2
- Update to 2.91.8
- Build the spice plugin

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.7-1
- Update to 2.91.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-2
- Disable the applet
- Build against gtk3

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-1
- Update to 2.31.4

* Sat Jun 19 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-2
- Reduce overlinking

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0
- Modernize the icon cache handling

* Tue Mar  9 2010 Tomas Bzatek <tbzatek@redhat.com> 2.29.92-1
- Update to 2.29.92

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91-1
- Update to 2.29.91

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-1
- Update to 2.29.90

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> 2.29.6-1
- Update to 2.29.6

* Mon Jan  4 2010 Matthias Clasen <mclasen@redhat.com> 2.29.1-2
- Don't crash when the history file is empty (#552076)

* Fri Dec  4 2009 Matthias Clasen <mclasen@redhat.com> 2.29.1-1
- 2.29.1

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-1
- Update to 2.28.1

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0.1-1
- Update to 2.28.0.1

* Fri Sep 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-3
- Update mDNS patch

* Fri Sep 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-2
- Fix mDNS bookmarks activation

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Sat Sep  5 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-3
- Fix warnings at startup (#521382)

* Thu Sep  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-2
- Make ids unique

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- 2.27.90

* Tue Aug 04 2009 Bastien Nocera <bnocera@redhat.com> 2.27.5-2
- Fix pkg-config requires

* Tue Jul 28 2009 Matthisa Clasen <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5
- Split off a -devel package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/vinagre/2.26/vinagre-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Fri Jan 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-2
- Better URL
- Tweak %%description

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Thu Oct  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Wed Jun 25 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.4-2
- Rebuild

* Tue Jun 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.4-1
- Update to 2.23.4
- Fix URL (#451746)

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3.1-1
- Update to 2.23.3.1

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.92-1
- Update to 0.4.92

* Mon Feb 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.91-2
- Spec file fixes

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.91-1
- Update to 0.4.91

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.90-1
- Update to 0.4.90

* Thu Dec 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.4-1
- Update to 0.4 and drop obsolete patches

* Fri Nov 23 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-3
- Fix crasher when passing broken options on the command-line (#394671)

* Thu Oct 25 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-2
- Fix crasher when setting a favourite with no password (#352371)

* Mon Sep 24 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-1
- Update to 0.3

* Wed Aug 22 2007 - Bastien Nocera <bnocera@redhat.com> - 0.2-1
- First version
- Fix plenty of comments from Ray Strode as per review
- Have work-around for BZ #253734

