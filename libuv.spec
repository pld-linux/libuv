#
# Conditional build:
%bcond_with	tests		# build with tests (require network access)

Summary:	Platform layer for node.js
Name:		libuv
Version:	0.10.29
Release:	1
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
Group:		Development/Tools
Source0:	http://libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	e9f82bbee67c1c468cd33dc869d306e3
Source2:	%{name}.pc.in
URL:		http://nodejs.org/
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-gyp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# we only need major.minor in the SONAME in the stable (even numbered) series
# this should be changed to %{version} in unstable (odd numbered) releases
%define		sover	0.10

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

%build
CC="%{__cc}" \
CXX="%{__cxx}" \
LDFLAGS="%{rpmldflags}" \
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
./gyp_uv.py \
	-Dcomponent=shared_library \
	-Dlibrary=shared_library

%{__make} V=1 -C out \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	BUILDTYPE=Release \
	CC.host="%{__cc}" \
	CXX.host="%{__cxx}" \
	LDFLAGS.host="%{rpmldflags}"

%if %{with tests}
./run-tests
./run-benchmarks
%endif

%install
rm -rf $RPM_BUILD_ROOT
# Copy the shared lib into the libdir
install -d $RPM_BUILD_ROOT%{_libdir}
cp -p out/Release/obj.target/libuv.so $RPM_BUILD_ROOT%{_libdir}/libuv.so.%{version}
lib=$(basename $RPM_BUILD_ROOT%{_libdir}/libuv.so.*.*.*)
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libuv.so.%{sover}
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libuv.so

# Copy the headers into the include path
install -d $RPM_BUILD_ROOT/%{_includedir}/uv-private
cp -p include/uv.h $RPM_BUILD_ROOT/%{_includedir}
cp -p \
   include/uv-private/ngx-queue.h \
   include/uv-private/tree.h \
   include/uv-private/uv-linux.h \
   include/uv-private/uv-unix.h \
   $RPM_BUILD_ROOT/%{_includedir}/uv-private

# Create the pkgconfig file
install -d $RPM_BUILD_ROOT/%{_pkgconfigdir}
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %{SOURCE2} > $RPM_BUILD_ROOT%{_pkgconfigdir}/libuv.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS LICENSE
%attr(755,root,root) %{_libdir}/libuv.so.*.*.*
%ghost %{_libdir}/libuv.so.%{sover}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libuv.so
%{_pkgconfigdir}/libuv.pc
%{_includedir}/uv.h
%{_includedir}/uv-private
