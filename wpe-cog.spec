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
Version:	0.18.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://wpewebkit.org/releases/cog-%{version}.tar.xz
# Source0-md5:	0566ab6676b499ebcff372fbe39e24fc
URL:		https://wpewebkit.org/
BuildRequires:	gcc >= 5:3.2
%{!?with_libsoup3:BuildRequires:	glib2-devel >= 1:2.44}
%{?with_libsoup3:BuildRequires:	glib2-devel >= 1:2.67.4}
BuildRequires:	libepoxy-devel
BuildRequires:	libmanette-devel >= 0.2.4
%{!?with_libsoup3:BuildRequires:	libsoup-devel >= 2.4}
%{?with_libsoup3:BuildRequires:	libsoup3-devel >= 3.0}
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libwpe-devel >= 1.14
BuildRequires:	meson >= 0.53.2
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
%{!?with_libsoup3:BuildRequires:	wpe-webkit-devel >= 2.34}
%{?with_libsoup3:BuildRequires:	wpe-webkit2-devel >= 2.40}
BuildRequires:	wpebackend-fdo-devel >= 1.8.0
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
%endif
%if %{with gtk4}
BuildRequires:	gtk4-devel >= 4.0
%endif
%if %{with wayland}
BuildRequires:	EGL-devel
BuildRequires:	cairo-devel
# wayland-client wayland-cursor
BuildRequires:	wayland-devel >= 1.10
BuildRequires:	wayland-egl-devel
BuildRequires:	wayland-protocols
BuildRequires:	xorg-lib-libxkbcommon-devel
%if %{with weston}
BuildRequires:	weston-protocols >= 13.0.0
%endif
%endif
%if %{with x11}
BuildRequires:	EGL-devel
BuildRequires:	libxcb-devel
BuildRequires:	xorg-lib-libxkbcommon-x11-devel
%endif
Requires:	wpebackend-fdo >= 1.8.0
Requires:	%{name}-libs = %{version}-%{release}
%if %{with drm}
Requires:	Mesa-libgbm >= 13.0
Requires:	libdrm >= 2.4.71
%endif
%if %{with wayland}
Requires:	wayland >= 1.10
Requires:	wpebackend-fdo >= 1.6.0
%if %{with weston}
Requires:	weston >= 13
%endif
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
%{!?with_libsoup3:Requires:	wpe-webkit >= 2.34}
%{?with_libsoup3:Requires:	wpe-webkit2 >= 2.40}

%description libs
Cog Core library.

%description libs -l pl.UTF-8
Biblioteka Cog Core.

%package devel
Summary:	Header files for Cog Core library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Cog Core
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{!?with_libsoup3:Requires:	wpe-webkit-devel >= 2.34}
%{?with_libsoup3:Requires:	wpe-webkit2-devel >= 2.40}

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
PLATFORMS="%{?with_drm:drm} %{?with_headless:headless} %{?with_wayland:wayland} %{?with_gtk4:gtk4} %{?with_x11:x11}"
%meson build \
	-Dcog_home_uri:-Dcog_home_uri="https://www.pld-linux.org/" \
	%{?with_apidocs:-Ddocumentation=true} \
	-Dplatforms="$(echo $PLATFORMS | sed -e 's/ \+/,/g')" \
	%{?with_weston:-Dwayland_weston_direct_display=true} \
	-Dwpe_api=%{?with_libsoup3:2.0}%{!?with_libsoup3:1.0} \
# -Dwayland_weston_content_protection=true ?

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%attr(755,root,root) %ghost %{_libdir}/libcogcore.so.9

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
