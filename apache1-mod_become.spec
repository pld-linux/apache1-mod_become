%define		mod_name	become
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: Become Somebody
Summary(pl):	Modu� Apache'a: stawanie si� kim�
Name:		apache1-mod_%{mod_name}
Version:	1.3
Release:	1.4
License:	?
Group:		Networking/Daemons
Source0:	http://www.snert.com/Software/mod_become/mod_become103.tgz
# Source0-md5:	7bb1607587687dabc711b3b1903947e5
URL:		http://www.snert.com/Software/mod_become/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	%{apxs}
Requires(triggerpostun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This module enables the web server to take on the access rights of a
user & group, so that users can make available files to the web
without having to make them readable by the world on the local file
system. This can be useful for sites with a large number of users who
want to apply file access controls among themselves. This module can
also be applied to virtual hosts, directories, and locations.

%description -l pl
Ten modu� pozwala serwerowi WWW przej�� prawa dost�pu u�ytkownika i
grupy, dzi�ki czemu u�ytkownicy mog� udost�pni� pliki na WWW bez
czynienia ich globalnie czytelnymi w lokalnym systemie plik�w. Mo�e to
by� przydatne na dla serwer�w z du�� liczb� u�ytkownik�w, kt�rzy chc�
kontrolowa� dost�p do plik�w mi�dzy sob�. Ten modu� mo�e by� u�ywany
tak�e z serwerami wirtualnymi, katalogami i miejscami.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
PATH=$PATH:%{_sbindir}
%{__make} build-dynamic \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo '#LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "mod_%{mod_name}: This module is not turned on by default; if you're sure,"
echo "mod_%{mod_name}: uncomment the appropriate line in Apache's config file."

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1.3-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt SECURITY.txt index.shtml notes-conf.txt
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
