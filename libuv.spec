#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	tests		# build with tests (require network access)

Summary:	Multi-platform support library with a focus on asynchronous I/O
Summary(pl.UTF-8):	Wieloplatformowa biblioteka wspierająca skupiająca się na asynchronicznym we/wy
Name:		libuv
Version:	1.34.2
Release:	1
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
Group:		Libraries
Source0:	https://dist.libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	a10243f691f7707f1d903d80e347b549
URL:		http://libuv.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.12
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libuv is a multi-platform support library with a focus on asynchronous
I/O. It was primarily developed for use by Node.js, but it's also used
by Luvit, Julia, pyuv and others.

%description -l pl.UTF-8
libuv to wieloplatformowa biblioteka wspierająca, skupiająca się na
asynchronicznych operacjach wejścia-wyjścia. Była rozwijana głównie z
myślą o wykorzystaniu w Node.js, ale obecnie jest używana także przez
projekty takie jak Luvit, Julia, pyuv i inne.

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
%{_includedir}/uv.h
%{_includedir}/uv
%{_pkgconfigdir}/libuv.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libuv.a
%endif
