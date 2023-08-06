Name: liblnk
Version: 20181120
Release: 1
Summary: Library to access the Windows Shortcut File (LNK) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/liblnk
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
               
BuildRequires: gcc               

%description -n liblnk
Library to access the Windows Shortcut File (LNK) format

%package -n liblnk-devel
Summary: Header files and libraries for developing applications for liblnk
Group: Development/Libraries
Requires: liblnk = %{version}-%{release}

%description -n liblnk-devel
Header files and libraries for developing applications for liblnk.

%package -n liblnk-python2
Obsoletes: liblnk-python < %{version}
Provides: liblnk-python = %{version}
Summary: Python 2 bindings for liblnk
Group: System Environment/Libraries
Requires: liblnk = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n liblnk-python2
Python 2 bindings for liblnk

%package -n liblnk-python3
Summary: Python 3 bindings for liblnk
Group: System Environment/Libraries
Requires: liblnk = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n liblnk-python3
Python 3 bindings for liblnk

%package -n liblnk-tools
Summary: Several tools for reading Windows Shortcut Files (LNK)
Group: Applications/System
Requires: liblnk = %{version}-%{release}

%description -n liblnk-tools
Several tools for reading Windows Shortcut Files (LNK)

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

%files -n liblnk
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n liblnk-devel
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblnk.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n liblnk-python2
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n liblnk-python3
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n liblnk-tools
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Dec 15 2018 Joachim Metz <joachim.metz@gmail.com> 20181120-1
- Auto-generated

