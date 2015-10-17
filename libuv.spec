#
# Conditional build:
%bcond_with	tests		# build with tests (require network access)

Summary:	Platform layer for node.js
Name:		libuv
Version:	1.0.2
Release:	1
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
Group:		Development/Tools
Source0:	http://dist.libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	3507961d2f06f1e35906a83ffe7f9f4c
URL:		http://libuv.org/
BuildRequires:	automake >= 1:1.12
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-gyp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libuv is a new platform layer for Node. Its purpose is to abstract
IOCP on Windows and libev on Unix systems. We intend to eventually
contain all platform differences in this library.

%package devel
Summary:	Development libraries for libuv
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries for libuv.

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
	--disable-silent-rules \
	--disable-static
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
%doc README.md AUTHORS LICENSE
%attr(755,root,root) %{_libdir}/libuv.so.*.*.*
%ghost %{_libdir}/libuv.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libuv.so
%{_pkgconfigdir}/libuv.pc
%{_includedir}/uv.h
%{_includedir}/uv-errno.h
%{_includedir}/uv-linux.h
%{_includedir}/uv-threadpool.h
%{_includedir}/uv-unix.h
%{_includedir}/uv-version.h
