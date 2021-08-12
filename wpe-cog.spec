#
# Conditional build:
%bcond_with	gtk		# WebKitGTK+ instead of WPEWebKit
%bcond_without	drm		# DRM platform module
%bcond_without	fdo		# FDO platform module
%bcond_with	weston		# direct display support for FDO platform module (requires private protocol files)
#
%if %{with gtk}
%undefine	with_drm
%undefine	with_fdo
%undefine	with_weston
%endif
Summary:	Cog Core - WPE WebKit base launcher
Summary(pl.UTF-8):	Cog Core - narzędzie do uruchamiania środowiska WPE WebKit
Name:		wpe-cog
Version:	0.8.1
Release:	3
License:	MIT
Group:		Libraries
Source0:	https://wpewebkit.org/releases/cog-%{version}.tar.xz
# Source0-md5:	21664fb04c9149dea6d68e13e6074276
Patch0:		cog-link.patch
URL:		https://wpewebkit.org/
BuildRequires:	cmake >= 3.3
BuildRequires:	gcc >= 5:3.2
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with gtk}
BuildRequires:	gtk-webkit4-devel >= 2.20.0
%else
BuildRequires:	wpe-webkit-devel >= 2.28.0
%if %{with drm}
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libgbm-devel >= 13.0
BuildRequires:	libdrm-devel >= 2.4.71
BuildRequires:	libinput-devel
BuildRequires:	udev-devel
BuildRequires:	wayland-devel
BuildRequires:	wpebackend-fdo-devel >= 1.3.1
%endif
%if %{with fdo}
BuildRequires:	EGL-devel
BuildRequires:	wayland-devel >= 1.10
BuildRequires:	wayland-egl-devel
BuildRequires:	wpebackend-fdo-devel >= 1.3.1
BuildRequires:	xorg-lib-libxkbcommon-devel
%if %{with weston}
BuildRequires:	weston-protocols >= 9.0.0
%endif
%endif
%endif
Requires:	%{name}-libs = %{version}-%{release}
%if %{with drm}
Requires:	Mesa-libgbm >= 13.0
Requires:	libdrm >= 2.4.71
Requires:	wpebackend-fdo >= 1.3.1
%endif
%if %{with fdo}
Requires:	wayland >= 1.10
Requires:	wpebackend-fdo >= 1.3.1
%if %{with weston}
Requires:	weston >= 9
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
Requires:	glib2 >= 1:2.44
%if %{with gtk}
Requires:	gtk-webkit4 >= 2.20.0
%else
Requires:	wpe-webkit >= 2.28.0
%endif

%description libs
Cog Core library.

%description libs -l pl.UTF-8
Biblioteka Cog Core.

%package devel
Summary:	Header files for Cog Core library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Cog Core
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%if %{with gtk}
Requires:	gtk-webkit4-devel >= 2.20.0
%else
Requires:	wpe-webkit-devel >= 2.28.0
%endif

%description devel
Header files for Cog Core library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Cog Core.

%prep
%setup -q -n cog-%{version}
%patch0 -p1

%build
install -d build
cd build
# .pc file creation expects relative CMAKE_INSTALL_LIBDIR
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCOG_HOME_URI="https://www.pld-linux.org/" \
	%{?with_drm:-DCOG_PLATFORM_DRM=ON} \
	%{!?with_fdo:-DCOG_PLATFORM_FDO=OFF} \
	%{?with_gtk:-DCOG_USE_WEBKITGTK=ON} \
	%{?with_weston:-DCOG_WESTON_DIRECT_DISPLAY=ON}

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
%doc ARCHITECTURE.md COPYING NEWS README.md
%attr(755,root,root) %{_bindir}/cog
%attr(755,root,root) %{_bindir}/cogctl
%if %{with drm}
%attr(755,root,root) %{_libdir}/libcogplatform-drm.so
%endif
%if %{with fdo}
%attr(755,root,root) %{_libdir}/libcogplatform-fdo.so
%endif
%{_mandir}/man1/cog.1*
%{_mandir}/man1/cogctl.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcogcore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcogcore.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcogcore.so
%{_includedir}/cog
%{_pkgconfigdir}/cogcore.pc
