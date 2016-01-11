#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	tests		# build with tests (require network access)

Summary:	Platform layer for node.js
Summary(pl.UTF-8):	Zależna od platformy warstwa node.js
Name:		libuv
Version:	1.6.1
Release:	2
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
Group:		Libraries
Source0:	http://dist.libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	51cfa3d8adc05852982e3c742ec3c039
URL:		http://libuv.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.12
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libuv is a new platform layer for Node. Its purpose is to abstract
IOCP on Windows and libev on Unix systems. We intend to eventually
contain all platform differences in this library.

%description -l pl.UTF-8
libuv to nowa, zależna od platformy warstwa Node. Celem jest
abstrakcja dla IOCP na Windows i libev na systemach uniksowych. W
przyszłości ta biblioteka może zawierać wszystkie różnice
międzyplatformowe.

%package devel
Summary:	Header files for libuv library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libuv
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries for libuv.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libuv.

%package static
Summary:	Static libuv library
Summary(pl.UTF-8):	Statyczna biblioteka libuv
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libuv library.

%description static -l pl.UTF-8
Statyczna biblioteka libuv.

%prep
%setup -q -n %{name}-v%{version}

# serial-tests is available in v1.12 and newer.
echo "m4_define([UV_EXTRA_AUTOMAKE_FLAGS], [serial-tests])" > m4/libuv-extra-automake-flags.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	ac_cv_lib_nsl_gethostbyname=no \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
./run-tests
./run-benchmarks
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by .pc file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libuv.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README.md
%attr(755,root,root) %{_libdir}/libuv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuv.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuv.so
%{_pkgconfigdir}/libuv.pc
%{_includedir}/uv.h
%{_includedir}/uv-errno.h
%{_includedir}/uv-linux.h
%{_includedir}/uv-threadpool.h
%{_includedir}/uv-unix.h
%{_includedir}/uv-version.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libuv.a
%endif
