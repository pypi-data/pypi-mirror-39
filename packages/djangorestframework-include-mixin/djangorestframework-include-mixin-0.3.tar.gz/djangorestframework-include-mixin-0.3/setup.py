import os
import re

from setuptools import setup


def get_version(package):
    with open(os.path.join(package, '__init__.py'), 'rb') as init_py:
        src = init_py.read().decode('utf-8')
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", src).group(1)


name = 'djangorestframework-include-mixin'
package = 'rest_framework_include_mixin'
version = get_version(package)
description = 'Optimized includable serializer fields.'
url = 'https://github.com/art1415926535/django-rest-framework-include-mixin'
author = 'Artem Fedotov'
author_email = 'badum-ts@yandex.ru'
license = 'MIT'
install_requires = [
    'djangorestframework>=3.0.0',
]


def read(*paths):
    """Build a file path from paths and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


def get_packages(package):
    """Return root package and all sub-packages."""
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, '__init__.py'))
    ]


def get_package_data(package):
    """Return all files under the root package."""
    walk = [
        (dirpath.replace(package + os.sep, '', 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(os.path.join(dirpath, '__init__.py'))
    ]

    file_paths = []
    for base, filenames in walk:
        file_paths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: file_paths}


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=install_requires,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
