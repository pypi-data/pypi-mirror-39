Name: libregf
Version: 20181129
Release: 1
Summary: Library to access the Windows NT Registry File (REGF) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libregf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
              
BuildRequires: gcc              

%description -n libregf
Library to access the Windows NT Registry File (REGF) format

%package -n libregf-devel
Summary: Header files and libraries for developing applications for libregf
Group: Development/Libraries
Requires: libregf = %{version}-%{release}

%description -n libregf-devel
Header files and libraries for developing applications for libregf.

%package -n libregf-python2
Obsoletes: libregf-python < %{version}
Provides: libregf-python = %{version}
Summary: Python 2 bindings for libregf
Group: System Environment/Libraries
Requires: libregf = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libregf-python2
Python 2 bindings for libregf

%package -n libregf-python3
Summary: Python 3 bindings for libregf
Group: System Environment/Libraries
Requires: libregf = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libregf-python3
Python 3 bindings for libregf

%package -n libregf-tools
Summary: Several tools for reading Windows NT Registry Files (REGF)
Group: Applications/System
Requires: libregf = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libregf-tools
Several tools for reading Windows NT Registry Files (REGF)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libregf
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libregf-devel
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libregf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libregf-python2
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libregf-python3
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libregf-tools
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Thu Nov 29 2018 Joachim Metz <joachim.metz@gmail.com> 20181129-1
- Auto-generated

