Name: libevt
Version: 20181216
Release: 1
Summary: Library to access the Windows Event Log (EVT) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libevt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
                
BuildRequires: gcc                

%description -n libevt
Library to access the Windows Event Log (EVT) format

%package -n libevt-devel
Summary: Header files and libraries for developing applications for libevt
Group: Development/Libraries
Requires: libevt = %{version}-%{release}

%description -n libevt-devel
Header files and libraries for developing applications for libevt.

%package -n libevt-python2
Obsoletes: libevt-python < %{version}
Provides: libevt-python = %{version}
Summary: Python 2 bindings for libevt
Group: System Environment/Libraries
Requires: libevt = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libevt-python2
Python 2 bindings for libevt

%package -n libevt-python3
Summary: Python 3 bindings for libevt
Group: System Environment/Libraries
Requires: libevt = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libevt-python3
Python 3 bindings for libevt

%package -n libevt-tools
Summary: Several tools for reading Windows Event Log (EVT) files
Group: Applications/System
Requires: libevt = %{version}-%{release}     
     

%description -n libevt-tools
Several tools for reading Windows Event Log (EVT) files

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

%files -n libevt
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libevt-devel
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libevt.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libevt-python2
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libevt-python3
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libevt-tools
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Dec 16 2018 Joachim Metz <joachim.metz@gmail.com> 20181216-1
- Auto-generated

