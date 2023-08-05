# -*- coding: utf-8 -*-

import gddriver

try:
    import setuptools
except ImportError:
    import distutils.core as setuptools

requirements = [
    'crcmod',
    'oss2>=2.4.0'
]
test_requirements = ['mock']

packages = setuptools.find_packages(exclude=['tests', 'tests.*'])
setuptools.setup(
    name='gddriver',
    description="The gddriver is an efficient tool for operating the storage service such as oss and ftp.",
    version=gddriver.VERSION,
    author='GeneDock Contributor',
    author_email="lixiarong@genedock.com",
    maintainer='GeneDock Contributor',
    maintainer_email='lixiarong@genedock.com',
    url='https://genedock.com',
    packages=packages,
    package_data={'': ['LICENSE', 'requirements.txt']},
    license='ASF',

    platforms=['Independent'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    tests_require=test_requirements,
    test_suite='tests'
)
