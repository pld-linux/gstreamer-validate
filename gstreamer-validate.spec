%define		gst_ver		1.14.0
%define		gstpb_ver	1.14.0
Summary:	GstValidate - suite of tools to run GStreamer integration tests
Summary(pl.UTF-8):	GstValidate - zestaw narzędzi do uruchamiania testów integracyjnych GStreamera
Name:		gstreamer-validate
Version:	1.14.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-validate/gst-validate-%{version}.tar.xz
# Source0-md5:	1f4fc5308695adfdc11d13046aa4888c
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	cairo-devel
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	json-glib-devel >= 1.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 1:2.7.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.36.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Requires:	json-glib >= 1.0
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of GstValidate is to be able to detect when elements are not
behaving as expected and report it to the user so he knows how things
are supposed to work inside a GstPipeline. In the end, fixing issues
found by the tool will ensure that all elements behave all together in
the expected way.

%description -l pl.UTF-8
Celem GstValidate jest umożliwienie wykrycia sytuacji, kiedy elementy
nie zachowują się w sposób oczekiwany i zgłaszanie tego faktu
użytkownikowi tak, aby wiedział, jak powinny działać elementy wewnątrz
GstPipeline. W efekcie, poprawienie problemów wykrytych przez to
narzędzie zapewni, że wszystkie elementy razem będą się zachowywały w
sposób zgodny z oczekiwaniami.

%package devel
Summary:	Header files for GstValidate library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GstValidate
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0
Requires:	gstreamer-devel >= %{gst_ver}
Requires:	gstreamer-plugins-base-devel >= %{gstpb_ver}

%description devel
Header files for GstValidate library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GstValidate.

%package apidocs
Summary:	API documentation for GstValidate library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GstValidate
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for GstValidate library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GstValidate.

%prep
%setup -q -n gst-validate-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
# disable sphinx for now: docs/launcher/conf.py is missing
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	--disable-sphinx-doc \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
# modules loaded through glib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgstvalidatetracer.la \
	$RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/validate/libgstvalidate*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gst-validate-1.0
%attr(755,root,root) %{_bindir}/gst-validate-images-check-1.0
%attr(755,root,root) %{_bindir}/gst-validate-launcher
%attr(755,root,root) %{_bindir}/gst-validate-media-check-1.0
%attr(755,root,root) %{_bindir}/gst-validate-transcoding-1.0
%attr(755,root,root) %{_libdir}/libgstvalidate-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvalidate-1.0.so.0
%attr(755,root,root) %{_libdir}/libgstvalidate-default-overrides-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvalidate-default-overrides-1.0.so.0
%attr(755,root,root) %{_libdir}/libgstvalidatevideo-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstvalidatevideo-1.0.so.0
%{_libdir}/girepository-1.0/GstValidate-1.0.typelib
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstvalidatetracer.so
%dir %{_libdir}/gstreamer-1.0/validate
%attr(755,root,root) %{_libdir}/gstreamer-1.0/validate/libgstvalidatefaultinjection.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/validate/libgstvalidategapplication.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/validate/libgstvalidategtk.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/validate/libgstvalidatessim.so
%{_libdir}/gst-validate-launcher
%dir %{_datadir}/gstreamer-1.0
%{_datadir}/gstreamer-1.0/validate

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstvalidate-1.0.so
%attr(755,root,root) %{_libdir}/libgstvalidate-default-overrides-1.0.so
%attr(755,root,root) %{_libdir}/libgstvalidatevideo-1.0.so
%{_includedir}/gstreamer-1.0/gst/validate
%dir %{_includedir}/gstreamer-1.0/lib
%{_includedir}/gstreamer-1.0/lib/validate
%{_pkgconfigdir}/gst-validate-1.0.pc
%{_datadir}/gir-1.0/GstValidate-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gst-validate-1.0
%{_gtkdocdir}/gst-validate-plugins-1.0
