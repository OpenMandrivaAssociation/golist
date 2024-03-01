%global debug_package %{nil}

%bcond_without bootstrap2

# Run tests in check section
%bcond_without check

# https://pagure.io/golist
%global goipath		pagure.io/golist
%global forgeurl	https://pagure.io/golist
Version:			0.10.4

%gometa

Summary:	A tool to analyse the properties of a Go (Golang) codebase
Name:		golist
Release:	1

Source0:	https://pagure.io/golist/archive/v%{version}/golist-%{version}.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golist-package-dependencies.sh
%endif
License:	BSD-3-Clause
URL:		https://pagure.io/golist

BuildRequires:	compiler(go-compiler)
%if ! %{with bootstrap2}
BuildRequires:	golang(github.com/urfave/cli)
%endif

%description
golist is a small utility used to list the resources required
and provided by a Go (Golang) project.

%files
%doc README.md NEWS.md
%license LICENSE
%{_bindir}/golist

#-----------------------------------------------------------------------

%prep
%autosetup -p1

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

%build
%gobuildroot
for cmd in cmd/* ; do
	%gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
install -dpm 0755 %{buildroot}%{_bindir}/
install -Dpm 0755 %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%check
%if %{with check}
%gochecks
%endif

