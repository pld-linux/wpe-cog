#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	drm		# DRM platform module
%bcond_without	gtk4		# GTK4 platform module
%bcond_without	headless	# headless platform module
%bcond_without	wayland		# Wayland (FDO) platform module
%bcond_without	x11		# X11 platform module
%bcond_with	libsoup3	# libsoup3 instead of libsoup 2.x
%bcond_with	weston		# direct display support for FDO platform module (requires private protocol files)
#
Summary:	Cog Core - WPE WebKit base launcher
Summary(pl.UTF-8):	Cog Core - narzędzie do uruchamiania środowiska WPE WebKit
Name:		wpe-cog
Version:	0.12.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://wpewebkit.org/releases/cog-%{version}.tar.xz
# Source0-md5:	cdb8acdc3acc9b5082e7db9c279155c3
URL:		https://wpewebkit.org/
BuildRequires:	cmake >= 3.3
BuildRequires:	gcc >= 5:3.2
%{!?with_libsoup3:BuildRequires:	glib2-devel >= 1:2.44}
%{?with_libsoup3:BuildRequires:	glib2-devel >= 1:2.67.4}
%{!?with_libsoup3:BuildRequires:	libsoup-devel >= 2.4}
%{?with_libsoup3:BuildRequires:	libsoup3-devel >= 3.0}
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
%{!?with_libsoup3:BuildRequires:	wpe-webkit-devel >= 2.28.0}
%{?with_libsoup3:BuildRequires:	wpe-webkit1.1-devel >= 2.33.1}
BuildRequires:	wpe-webkit-devel >= 2.28.0
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	gobject-introspection-devel
BuildRequires:	gi-docgen
%endif
%if %{with drm}
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libgbm-devel >= 13.0
BuildRequires:	libdrm-devel >= 2.4.71
BuildRequires:	libinput-devel
BuildRequires:	udev-devel
# wayland-server
BuildRequires:	wayland-devel
BuildRequires:	wpebackend-fdo-devel >= 1.4.0
%endif
%if %{with gtk4}
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	wpebackend-fdo-devel
%endif
%if %{with headless}
BuildRequires:	wpebackend-fdo-devel >= 1.8.0
%endif
%if %{with wayland}
BuildRequires:	EGL-devel
BuildRequires:	cairo-devel
# wayland-client wayland-cursor
BuildRequires:	wayland-devel >= 1.10
BuildRequires:	wayland-egl-devel
BuildRequires:	wayland-protocols
BuildRequires:	wpebackend-fdo-devel >= 1.6.0
BuildRequires:	xorg-lib-libxkbcommon-devel
%if %{with weston}
BuildRequires:	weston-protocols >= 9.0.0
%endif
%endif
%if %{with x11}
BuildRequires:	EGL-devel
BuildRequires:	libxcb-devel
BuildRequires:	wpebackend-fdo-devel >= 1.6.0
BuildRequires:	xorg-lib-libxkbcommon-x11-devel
%endif
Requires:	%{name}-libs = %{version}-%{release}
%if %{with drm}
Requires:	Mesa-libgbm >= 13.0
Requires:	libdrm >= 2.4.71
Requires:	wpebackend-fdo >= 1.4.0
%endif
%if %{with headless}
BuildRequires:	wpebackend-fdo >= 1.8.0
%endif
%if %{with wayland}
Requires:	wayland >= 1.10
Requires:	wpebackend-fdo >= 1.6.0
%if %{with weston}
Requires:	weston >= 9
%endif
%endif
%if %{with x11}
Requires:	wpebackend-fdo >= 1.6.0
%endif
# cog in PLD used to be different project: http://www.krakoa.dk/old-linux-software.html#COG
Conflicts:	cog
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cog Core - WPE WebKit base launcher.

%description -l pl.UTF-8
Cog Core - narzędzie do uruchamiania środowiska WPE WebKit.

%package libs
Summary:	Cog Core library
Summary(pl.UTF-8):	Biblioteka Cog Core
Group:		Libraries
%{!?with_libsoup3:Requires:	glib2 >= 1:2.44}
%{?with_libsoup3:Requires:	glib2 >= 1:2.67.4}
%{!?with_libsoup3:Requires:	libsoup >= 2.4}
%{?with_libsoup3:Requires:	libsoup3 >= 3.0}
%{!?with_libsoup3:Requires:	wpe-webkit >= 2.28.0}
%{?with_libsoup3:Requires:	wpe-webkit1.1 >= 2.33.1}

%description libs
Cog Core library.

%description libs -l pl.UTF-8
Biblioteka Cog Core.

%package devel
Summary:	Header files for Cog Core library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Cog Core
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{!?with_libsoup3:Requires:	wpe-webkit-devel >= 2.28.0}
%{?with_libsoup3:Requires:	wpe-webkit1.1-devel >= 2.33.1}

%description devel
Header files for Cog Core library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Cog Core.

%package apidocs
Summary:	API documentation for Cog Core library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Cog Core
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Cog Core library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Cog Core.

%prep
%setup -q -n cog-%{version}

%build
install -d build
cd build
# .pc file creation expects relative CMAKE_INSTALL_LIBDIR
%cmake .. \
	%{?with_apidocs:-DBUILD_DOCS=ON} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCOG_HOME_URI="https://www.pld-linux.org/" \
	%{!?with_drm:-DCOG_PLATFORM_DRM=OFF} \
	%{?with_gtk4:-DCOG_PLATFORM_GTK4=ON} \
	%{!?with_headless:-DCOG_PLATFORM_HEADLESS=OFF} \
	%{!?with_wayland:-DCOG_PLATFORM_WL=OFF} \
	%{?with_x11:-DCOG_PLATFORM_X11=ON} \
	%{?with_gtk4:-DCOG_USE_WEBKITGTK=ON} \
	%{?with_weston:-DCOG_WESTON_DIRECT_DISPLAY=ON} \
	%{?with_libsoup3:-DUSE_SOUP2=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.md
%attr(755,root,root) %{_bindir}/cog
%attr(755,root,root) %{_bindir}/cogctl
%dir %{_libdir}/cog
%dir %{_libdir}/cog/modules
%attr(755,root,root) %{_libdir}/cog/modules/libcogplatform-headless.so
%if %{with drm}
%attr(755,root,root) %{_libdir}/cog/modules/libcogplatform-drm.so
%endif
%if %{with gtk4}
%attr(755,root,root) %{_libdir}/cog/modules/libcogplatform-gtk4.so
%endif
%if %{with wayland}
%attr(755,root,root) %{_libdir}/cog/modules/libcogplatform-wl.so
%endif
%if %{with x11}
%attr(755,root,root) %{_libdir}/cog/modules/libcogplatform-x11.so
%endif
%{_mandir}/man1/cog.1*
%{_mandir}/man1/cogctl.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcogcore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcogcore.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcogcore.so
%{_includedir}/cog
%{_pkgconfigdir}/cogcore.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/html/*
%endif
