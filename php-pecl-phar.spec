%define		_modname	phar
%define		_status		stable
Summary:	Extension to run complete applications out of .phar files (like Java .jar files)
Summary(pl.UTF-8):	Rozszerzenie do uruchamianie gotowych aplikacji z plików .phar (podobnych do .jar w Javie)
Name:		php-pecl-%{_modname}
Version:	2.0.0
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	fdba10432216c22c19cf8a86b3de56b9
URL:		http://pecl.php.net/package/phar/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-bzip2
Requires:	php-common >= 4:5.0.4
Requires:	php-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the extension version of PEAR's PHP_Archive package. Support
for zlib, bz2 and crc32 is achieved without any dependency other than
the external zlib or bz2 extension.

.phar files can be read using the phar stream, or with the Phar class.
If the SPL extension is available, a Phar object can be used as an
array to iterate over a phar's contents or to read files directly from
the phar.

Phar archives can be created using the streams API or with the Phar
class, if the phar.readonly ini variable is set to false.

Full support for MD5 and SHA1 signatures is possible. Signatures can
be required if the ini variable phar.require_hash is set to true. When
PECL extension hash is avaiable then SHA-256 and SHA-512 signatures
are supported as well.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie to odpowiednik klasy PEAR PHP_Archive. Obsługa metod
kompresji zlib, bz2 i crc32 została osiągnięta bez zależności innych
niż moduły zlib i bz2.

Pliki .phar mogą być odczytane przy użyciu strumienia phar lub za
pomocą klasy Phar. Jeśli rozszerzenie SPL jest dostępne, obiekt Phar
może być użyty jako tablica lub w celu bezpośredniego odczytu plików.

Archiwa Phar moga być stworzone przy użyciu API strumieni lub za
pomocą klasy Phar, jeśli zmienna phar.readonly jest ustawiona na
fałsz.

Pełne wsparcie dla skrótów MD5 i SHA1 jest możliwe. Skróty mogą być
wymagane, jeśli zmienna phar.require_hash ma wartość true. Jeśli
rozszerzenie PECL hash jest dostępne, możliwe jest także korzystanie
ze skrótów SHA-256 oraz SHA-512.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
