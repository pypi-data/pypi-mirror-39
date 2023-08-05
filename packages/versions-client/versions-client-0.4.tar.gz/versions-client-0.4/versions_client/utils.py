from __future__ import unicode_literals

import os
import platform
from datetime import datetime
from pkg_resources import working_set

import yaml

from envparse import env


def version(_name, _comment=True, **kwargs):
    label_list = [
        '{}="{}"'.format(str(label), str(value))
        for label, value in kwargs.items() if value]
    if not label_list:
        return None
    label_list.sort()
    labels = '{' + ','.join(label_list) + '}'
    comments = []
    if _comment:
        comments = [
            '# HELP version_{} version info.'.format(_name),
            '# TYPE version_{} gauge'.format(_name),
        ]
    return '\n'.join(comments + ['version_{}{} 1'.format(_name, labels)])


def os_package_list():
    versions = ''
    with open(os.environ.get('VERSIONS_OS_PACKAGE_PATH', '/var/local/os-package-versions.yaml'), 'r') as f:  # noqa
        versions = yaml.load(f)
    return versions


def get_distribution():
    try:
        env.read_envfile('/etc/os-release')
    except IOError:
        return {}

    distro_name = env('NAME')
    distro_version = env('VERSION_ID')
    distro_id = env('ID')

    if not distro_id:
        distro_id = distro_name

    distro_id = str(distro_id).lower().replace(' ', '-')

    try:
        # On Debian /etc/os-release only contains '8' as VERSION_ID
        # while /etc/debian_version contains '8.9'.
        with open('/etc/{}_version'.format(distro_id), 'r') as f:
            distro_version = f.readlines()[0].strip('\n')
    except IOError:
        pass

    return {
        'distro_name': distro_name.replace('_', ' '),
        'distro_version': distro_version,
        'distro_id': distro_id,
    }


def generate_versions(**application_labels):
    response = '\n'.join(filter(None, [
        version('application', **application_labels),
        version('platform', name=platform.system(), achitecture=platform.architecture()[0], type=platform.machine(), system=platform.release(), **get_distribution()),  # noqa
        version('python', version=platform.python_version(), date=datetime.strptime(platform.python_build()[1], '%b %d %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'), compiler=platform.python_compiler(), implementation=platform.python_implementation()),  # noqa
    ] + [version('package', group="os", name=package[0], version=package[1], _comment=key == 0) for key, package in enumerate(os_package_list().items())]  # noqa
      + [version('package', group="python", name=str(package.project_name).lower(), version=package._version, _comment=False) for package in working_set]  # noqa
    )) + '\n'
    return response.encode('utf-8')
