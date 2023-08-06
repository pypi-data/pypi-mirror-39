# Copyright (c) Microsoft Corporation. All rights reserved.
import copy
import distro
import glob
import os
import re
import shutil
import subprocess
import sys
from typing import List, Optional, Tuple


__version__ = '2.1.7'   # {major dotnet version}.{minor dotnet version}.{revision}
# We can rev the revision due to patch-level change in .net or changes in dependencies
missing_dep_re = re.compile(r'^(.+)\s*=>\s*not found\s*$', re.MULTILINE)


# https://github.com/dotnet/core/blob/master/Documentation/self-contained-linux-apps.md
# to evalute mappings candidates, run this cmd over the expanded dotnetcore runtime zip:
#   find . -name '*.so' | xargs ldd | less
# search for 'not found'.
ubuntu_mappings = {
    'libunwind-x86_64.so.8': 'libunwind8=1.1-4.1',
    'libunwind.so.8': 'libunwind8=1.1-4.1',
    'liblttng-ust.so.0': 'liblttng-ust0=2.7.1-1',
    'libcurl.so.4': 'libcurl3=7.47.0-1ubuntu2',
    'liburcu-bp.so.4': 'liburcu4=0.9.1-3',
    'liburcu-cds.so.4': 'liburcu4=0.9.1-3',
    'libgssapi_krb5.so.2': 'libgssapi-krb5-2',
    'libkrb5.so.3': 'libkrb5-3',
    'libkrb5support.so.0': 'libkrb5support0',
    'librtmp.so.1': 'librtmp1',
    'libk5crypto.so.3': 'libk5crypto3',
    'libldap_r-2.4.so.2': 'libldap-2.4-2',
    'libkeyutils.so.1': 'libkeyutils1',
    'liblber-2.4.so.2': 'libldap-2.4-2',
    'libssl.so.1.0.0': 'libssl1.0.0',
    'libcrypto.so.1.0.0': 'libcrypto++9v5',
    'libidn.so.11': 'libidn11',
    'libgnutls.so.30': 'libgnutls30',
    'libnettle.so.6': 'libnettle6',
    'libhogweed.so.4': 'libhogweed4',
    'libgssapi.so.3': 'libgssapi3-heimdal',
    'libsasl2.so.2': 'libsasl2-2',
    'libkrb5.so.26': 'libkrb5-26-heimdal',
    'libhcrypto.so.4': 'libhcrypto4-heimdal',
    'libp11-kit.so.0': 'libp11-kit0',
    'libheimntlm.so.0': 'libheimntlm0-heimdal',
    'libtasn1.so.6': 'libtasn1-6',
    'libroken.so.18': 'libroken18-heimdal',
    'libasn1.so.8': 'libasn1-8-heimdal',
    'libheimbase.so.1': 'libheimbase1-heimdal',
    'libffi.so.6': 'libffi6',
    'libhx509.so.5': 'libhx509-5-heimdal',
    'libwind.so.0': 'libwind0-heimdal',
    'libsqlite3.so.0': 'libsqlite3-0'
}

rhel_mappings = {
    'liblttng-ust.so.0': 'rh-dotnet21-lttng-ust.x86_64',
    'liburcu-bp.so.4': 'rh-dotnet21-userspace-rcu.x86_64',
    'liburcu-cds.so.4': 'rh-dotnet21-userspace-rcu.x86_64',
    'libcurl.so.4': 'rh-dotnet21-curl.x86_64'
}

centos_rpm_url_prefix = 'http://download.fedoraproject.org/pub/epel/7/x86_64/Packages/'
centos_mappings = {
    'liblttng-ust.so.0': 'lttng-ust-2.4.1-4.el7.x86_64',
    'liburcu-cds.so.1': 'userspace-rcu-0.7.16-1.el7.x86_64',
    'liburcu-bp.so.1': 'userspace-rcu-0.7.16-1.el7.x86_64'
}

distro = distro.linux_distribution(full_distribution_name=False)[0] if sys.platform == 'linux' else None


def _get_mappings():
    if distro == 'ubuntu':
        return ubuntu_mappings
    if distro == 'rhel':
        return rhel_mappings
    if distro == 'centos':
        return centos_mappings
    else:
        raise ValueError('Unsupported Linux distribution {0}'.format(distro))

def _get_dependency_pkg_name(dependency: str) -> Tuple[str]:
    dep_mappings = _get_mappings()
    if dependency not in dep_mappings:
        return (None, dependency)

    return (dep_mappings[dependency], None)


def _gather_dependencies(path: str, search_path: str=None) -> List[Tuple[str]]:
    libraries = glob.glob(os.path.realpath(os.path.join(path, '**', '*.so')), recursive=True)
    missing_deps = set()
    env = copy.copy(os.environ)
    if search_path is not None:
        env['LD_LIBRARY_PATH'] = search_path
    for library in libraries:
        ldd_output = subprocess.run(['ldd', library], cwd=path, stdout=subprocess.PIPE, env=env).stdout.decode('utf-8')
        matches = missing_dep_re.findall(ldd_output)
        missing_deps |= set(dep.strip() for dep in matches)

    return list(set(_get_dependency_pkg_name(dep) for dep in missing_deps))


def _install_dependency(pkg_name: str, target_path: str):
    download_folder = os.path.join(_get_pkg_download_folder(), pkg_name)
    os.makedirs(download_folder, exist_ok=True)
    downloader = _get_pkg_fetcher()
    downloader(pkg_name, download_folder)
    lib_files = glob.glob(os.path.join(download_folder, '**', '*.so*'), recursive=True)
    for file in lib_files:
        shutil.copy(file, target_path)

def _get_pkg_download_folder() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin', 'tmp')


def _get_bin_folder() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin')


def ensure_dependencies() -> Optional[str]:
    def _extract_truthy(arr: List[Tuple[str]], ind: int) -> List[str]:
        return list(set(filter(lambda elem: elem, map(lambda tup: tup[ind], arr))))

    if distro is None:
        return None

    bin_folder = _get_bin_folder()
    deps_path = os.path.join(bin_folder, 'deps')
    success_file = os.path.join(deps_path, 'SUCCESS-' + __version__)
    if os.path.exists(success_file):
         return deps_path

    os.makedirs(deps_path, exist_ok=True)
    while True:
        missing_pkgs = _gather_dependencies(bin_folder, search_path=deps_path)
        if not missing_pkgs:
            break

        found_packages = _extract_truthy(missing_pkgs, 0)
        not_found_packages = _extract_truthy(missing_pkgs, 1)

        if len(not_found_packages) > 0:
            sys.stderr.write('List of missing so:\n{}\n'.format('\n'.join(not_found_packages)))
            raise ValueError('Required so missing: {}'.format(not_found_packages))

        for pkg in found_packages:
            _install_dependency(pkg, deps_path)

    shutil.rmtree(_get_pkg_download_folder(), ignore_errors=True)
    with open(success_file, 'a'):
        os.utime(success_file, None)
    return deps_path


def get_runtime_path():
    search_string = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin', 'dotnet*')
    matches = [f for f in glob.glob(search_string, recursive=True)]
    return matches[0]


def _get_pkg_fetcher():
    if distro == 'ubuntu':
        return _fetch_deb_package
    if distro == 'rhel':
        return _fetch_yum_package
    if distro == 'centos':
        return _fetch_centos_epel_package
    else:
        return None

def _fetch_deb_package(pkg_name: str, download_folder: str):
    subprocess.run(['apt-get', 'download', pkg_name], cwd=download_folder)
    subprocess.run(['dpkg', '--extract', glob.glob(os.path.join(download_folder, '*.deb'))[0], './' + pkg_name],
                   cwd=download_folder)

def _fetch_centos_epel_package(pkg_name: str, download_folder: str):
    # Construct url for pkg_name located in EPEL fedora repository.
    # This would normally be done by yum, though the EPEL repo isn't on centos7 by default,
    # and we can't gurentee sudo privileges which are required to add a repo to yum. So
    # we need to do the work instead.
    pkgUrl = centos_rpm_url_prefix + pkg_name[0] + '/' + pkg_name + '.rpm'
    _fetch_rpm_url_package(pkgUrl, download_folder)

def _fetch_rpm_url_package(pkg_url: str, download_folder: str, cert_file: str = '', key_file: str = ''):
    if not _wget(pkg_url, cert_file, key_file, download_folder):
        if not _wget(pkg_url, cert_file, key_file, download_folder, use_sudo=True):
            raise ValueError('Cannot download yum package {0}'.format(pkg_url))

    # extract files:
    rpmProc = subprocess.Popen(['rpm2cpio', os.path.basename(pkg_url)], stdout=subprocess.PIPE, cwd=download_folder)
    cpioProc = subprocess.Popen(['cpio', '-idmv'], stdin=rpmProc.stdout, stdout=subprocess.PIPE, cwd=download_folder)
    rpmProc.stdout.close()
    cpioProc.communicate()

def _fetch_yum_package(pkg_name: str, download_folder: str):
    # gather package info needed for download from repo:
    pkg_info = subprocess.run(['yum', 'info', pkg_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True).stdout.decode('utf-8')
    repo_name_re = re.compile(r'^Repo\s*:\s*([a-zA-Z0-9_-]+)', re.MULTILINE)
    repo_name = repo_name_re.search(pkg_info)[1]
    if not repo_name:
        raise ValueError('Cannot find yum repo info for {0}'.format(pkg_name))

    repo_config_file = subprocess.run(['grep', '-F', '--color=never', '-l', '-r', repo_name, '/etc/yum.repos.d/'], stdout=subprocess.PIPE, check=True) \
        .stdout.decode('utf-8')
    if not repo_config_file:
        raise ValueError('Cannot find repo {0} in repo config files.'.format(repo_name))

    # parse out repo authN certificates from config:
    cert_file = ''
    key_file = ''
    with open(repo_config_file.strip(), 'r') as config:
        found_block = False
        for line in config:
            if found_block:
                if line.isspace():
                    break
                else:
                    line = line.strip()
                    if line.startswith('sslclientcert'):
                        cert_file = line.split('=')[1]
                    if line.startswith('sslclientkey'):
                        key_file = line.split('=')[1]
            else:
                if line.find(repo_name) >= 0:
                    found_block = True

    pkgUrl = subprocess.run(['repoquery', '--location', pkg_name], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()

    _fetch_rpm_url_package(pkgUrl, download_folder, cert_file, key_file)

def _wget(url: str, cert: str, key: str, cwd: str, use_sudo: bool=False) -> bool:
    wget_cmd = [ 'wget' ]
    if use_sudo:
        wget_cmd.insert(0, 'sudo')
    if cert and key:
        wget_cmd.extend([ '--no-check-certificate', '--certificate={}'.format(cert), '--private-key={}'.format(key)])
    wget_cmd.append(url)
    out = subprocess.run(wget_cmd, stderr=subprocess.PIPE, cwd=cwd, check=False).stderr.decode('utf-8')
    return out.find('200 OK') >= 0