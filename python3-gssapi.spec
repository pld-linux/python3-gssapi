# Conditional build:
%bcond_with	tests	# unit tests

%define		module	gssapi
Summary:	Python GSSAPI Wrapper
Name:		python3-%{module}
Version:	1.9.0
Release:	1
License:	ISCL
Group:		Libraries/Python
Source0:	https://pypi.debian.net/gssapi/gssapi-%{version}.tar.gz
# Source0-md5:	866fe5e21dcde16eb115d4e6ac526f06
URL:		https://pypi.org/project/gssapi/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-decorator
BuildRequires:	python3-flake8
BuildRequires:	python3-k5test
BuildRequires:	python3-mypy
BuildRequires:	python3-parametrized
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python-GSSAPI provides both low-level and high level wrappers around
the GSSAPI C libraries. While it focuses on the Kerberos mechanism, it
should also be useable with other GSSAPI mechanisms.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

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
%attr(755,root,root) %{py3_sitedir}/%{module}/raw/*.so
%{py3_sitedir}/%{module}/raw/__pycache__
%dir %{py3_sitedir}/%{module}/raw/_enum_extensions
%{py3_sitedir}/%{module}/raw/_enum_extensions/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/raw/_enum_extensions/*.so
%{py3_sitedir}/%{module}/raw/_enum_extensions/__pycache__
%dir %{py3_sitedir}/%{module}/tests
%{py3_sitedir}/%{module}/tests/*.py
%{py3_sitedir}/%{module}/tests/__pycache__
%{py3_sitedir}/%{module}-%{version}.dist-info
