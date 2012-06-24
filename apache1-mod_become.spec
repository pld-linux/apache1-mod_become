%define		mod_name	become
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: Become Somebody
Summary(pl):	Modu� Apache'a: stawanie si� kim�
Name:		apache-mod_%{mod_name}
Version:	1.3
Release:	1
License:	?
Group:		Networking/Daemons
Source0:	http://www.snert.com/Software/mod_become/mod_become103.tgz
# Source0-md5:	7bb1607587687dabc711b3b1903947e5
URL:		http://www.snert.com/Software/mod_become/
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

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
%{__make} build-dynamic

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt SECURITY.txt index.shtml notes-conf.txt
%attr(755,root,root) %{_pkglibdir}/*
