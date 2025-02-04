
%define plugin	muggle
%define name	vdr-plugin-%plugin
%define version	0.2.3
%define rel	2

# backportability
%define _localstatedir %{_var}

Summary:	VDR plugin: Media juggle
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPL
URL:		https://sourceforge.net/projects/vdr-muggle/
Source:		http://downloads.sourceforge.net/vdr-muggle/vdr-%plugin-%version.tgz
Patch0:		muggle-0.2.1-convert-location.patch
Patch1:		muggle-includes.patch
Patch4:		muggle-const-char-gcc4.4.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
Requires:	vdr-abi = %vdr_abi
BuildRequires:	mysql-static-devel
BuildRequires:	mad-devel
BuildRequires:	libtaglib-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libflac++-devel
BuildRequires:	libsndfile-devel
BuildRequires:	imlib2-devel
Requires:	mjpegtools
Requires:	netpbm

%description
The muggle plugin provides a database link for VDR so that selection
of media becomes more flexible.

%prep
%setup -q -n %plugin-%version
%patch0 -p1
%patch1 -p1
%patch4 -p1
sed -i 's,@MUGGLEDATADIR@,%{_vdr_plugin_datadir}/%{plugin},' mg_image_provider.c
%vdr_plugin_prep

%vdr_plugin_params_begin %plugin
# specify database name (default is GiantDisc)
var=DB_NAME
param="-n DB_NAME"
# specify toplevel directory for music (default is /mnt/music)
var=TOPLEVEL
param="-t TOPLEVEL"
# specify directory for embedded sql data (default is /var/lib/muggle)
var=DATADIR
param="-d DATADIR"
default=%{_localstatedir}/lib/muggle
# specify debug level. The higher the more. Default is 1
var=VERBOSE
param="-n VERBOSE"
# specify database host (default is embedded or localhost)
# if the specified host is localhost, sockets will
# be used if possible
# Otherwise the SOCKET parameter will be ignored
var=DB_HOST
param="-h DB_HOST"
# specify database socket
var=DB_SOCKET
param="-s DB_SOCKET"
# specify port of database server
var=DB_PORT
param="-p DB_PORT"
# specify database user
var=DB_USER
param="-u DB_USER"
# specify database password (default is empty)
# remember to chmod this file if you don't want the users to
# see the password
var=DB_PASSWORD
param="-w DB_PASSWORD"
%vdr_plugin_params_end

%build
# HAVE_FLAC=1 omitted, API incompatibility
%vdr_plugin_build HAVE_VORBISFILE=1 HAVE_SNDFILE=1 HAVE_FLAC=1 \
%if %mdkversion <= 200700
%ifnarch %ix86
	HAVE_ONLY_SERVER=1 # workaround for #24168
%endif
%endif

%install
rm -rf %{buildroot}
%vdr_plugin_install

install -d -m755 %{buildroot}%{_vdr_plugin_datadir}/%{plugin}
install -m755 scripts/muggle-image-convert %{buildroot}%{_vdr_plugin_datadir}/%{plugin}

install -d -m755 %{buildroot}%{_bindir}
install -m755 mugglei %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_localstatedir}/lib/muggle

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY README* TODO scripts
%{_vdr_plugin_datadir}/%{plugin}
%{_bindir}/mugglei
%attr(-,vdr,vdr) %dir %{_localstatedir}/lib/muggle
