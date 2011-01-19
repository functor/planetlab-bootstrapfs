# build is expected to export the following rpm variables
# %{distroname}     : e.g. Fedora
# %{distrorelease}  : e.g. 8
# %{slice_rpms_plus} : as a +++ separated list of rpms from the build dir

%define nodefamily %{pldistro}-%{distroname}-%{_arch}
%define obsolete_nodefamily %{pldistro}-%{_arch}

%define name slicerepo-%{nodefamily}
%define version 2.0
%define taglevel 6

# pldistro already in the rpm name
#%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}
%define release %{taglevel}%{?date:.%{date}}

Vendor: OneLab
Packager: PlanetLab Europe <build@onelab.eu>
Distribution: PlanetLab %{plrelease}
URL: %{SCMURL}

Summary: The yum repository for slices, to be installed on the myplc-side
Name: %{name}
Version: %{version}
Release: %{release}
License: BSD
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# other archs must be able to install this
BuildArch: noarch

BuildRequires: rsync 
Requires: myplc

%define debug_package %{nil}

%description
This rpm contains all the rpms that might ship on a sliver image
they come organized into a yum repository 

%prep
%setup -q

%build
echo nothing to do at build time for slicerepo

%install
rm -rf $RPM_BUILD_ROOT

repo=slice-%{nodefamily}
install -d -m 755 $RPM_BUILD_ROOT/var/www/html/install-rpms/$repo
rpms=$(echo %{slice_rpms_plus} | sed -e 's,+++, ,g')
for rpm in $rpms; do rsync %{_topdir}/$rpm $RPM_BUILD_ROOT/var/www/html/install-rpms/$repo/ ; done
### yumgroups
install -D -m 644 %{_topdir}/RPMS/yumgroups.xml $RPM_BUILD_ROOT/var/www/html/install-rpms/$repo/yumgroups.xml
# do not do this yet, as plc.d/packages will do it anyway
#createrepo -g yumgroups.xml $RPM_BUILD_ROOT/var/www/html/install-rpms/$repo

%clean
rm -rf $RPM_BUILD_ROOT

%post
service plc start packages

%files
%defattr(-,root,root,-)
/var/www/html/install-rpms/slice-%{nodefamily}
# don't overwrite yumgroups.xml if exists
%config(noreplace) /var/www/html/install-rpms/slice-%{nodefamily}/yumgroups.xml

%changelog
* Mon Jul 05 2010 Baris Metin <Talip-Baris.Metin@sophia.inria.fr> - BootstrapFS-2.0-6
- add sha1sum
- module name changes

* Tue Apr 27 2010 Talip Baris Metin <Talip-Baris.Metin@sophia.inria.fr> - BootstrapFS-2.0-5
- support different flavours of vservers on nodes

* Mon Apr 12 2010 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - BootstrapFS-2.0-4
- fix unmatched $ in URL svn keywords

* Fri Apr 02 2010 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - BootstrapFS-2.0-3
- choice between various pldistros is not made at build time, but at run time
- relies on GetNodeFlavour to expose the node's fcdistro - requires PLCAPI-5.0-5
- in addition, the baseurl for the myplc repo is http:// and not https:// anymore
- the https method does not work on fedora 12, and GPG is used below anyway

* Fri Mar 12 2010 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - BootstrapFS-2.0-2
- new slicerepo package for exposing stuff to slivers
