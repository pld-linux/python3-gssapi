#
# Conditional build:
%bcond_with	krb5	# MIT Kerberos instead of Heimdal
%bcond_with	tests	# unit tests

%define		module	gssapi
Summary:	Python GSSAPI Wrapper
Summary(pl.UTF-8):	Pythonowy interfejs do GSSAPI
Name:		python3-%{module}
Version:	1.11.1
Release:	1
License:	ISC
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/gssapi/
Source0:	https://files.pythonhosted.org/packages/source/g/gssapi/gssapi-%{version}.tar.gz
# Source0-md5:	70a141343b95b3e7d97a174b9ab52488
URL:		https://pypi.org/project/gssapi/
%if %{with krb5}
BuildRequires:	krb5-devel
%else
BuildRequires:	heimdal-devel
%endif
BuildRequires:	python3-Cython = 3.2.4
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools >= 1:40.6.0
%if %{with tests}
BuildRequires:	python3-decorator
BuildRequires:	python3-k5test
BuildRequires:	python3-parameterized
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python-GSSAPI provides both low-level and high level wrappers around
the GSSAPI C libraries. While it focuses on the Kerberos mechanism, it
should also be useable with other GSSAPI mechanisms.

%description -l pl.UTF-8
Python-GSSAPI udostępnia zarówno niskopoziomowe, jak i wysokopoziomowe
opakowanie bibliotek C GSSAPI. O ile skupia się na mechanizmie
Kerberos, powinien dać się używać także z innymi mechanizmami GSSAPI.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# avoid having .so-less gssapi dir in PWD
cd build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD" gssapi/tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/gssapi/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.*
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/py.typed
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/raw
%{py3_sitedir}/%{module}/raw/*.py
%{py3_sitedir}/%{module}/raw/*.pyi
%{py3_sitedir}/%{module}/raw/*.abi3.so
%{py3_sitedir}/%{module}/raw/__pycache__
%dir %{py3_sitedir}/%{module}/raw/_enum_extensions
%{py3_sitedir}/%{module}/raw/_enum_extensions/*.py
%{py3_sitedir}/%{module}/raw/_enum_extensions/*.abi3.so
%{py3_sitedir}/%{module}/raw/_enum_extensions/__pycache__
%{py3_sitedir}/%{module}-%{version}.dist-info
