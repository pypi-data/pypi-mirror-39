from setuptools import setup, find_packages

with open('README.rst', 'r') as inp:
    LONG_DESCRIPTION = inp.read()

setup(
    name='django_geoaxis',
    version='0.0.1',
    author='Boundless Spatial',
    author_email='contact@boundlessgeo.com',
    url='https://gitlab.devops.geointservices.io/boundlessgeo/django-geoaxis',
    download_url="https://gitlab.devops.geointservices.io/boundlessgeo/django-geoaxis",
    description="A Django authentication backend for GeoAxIS",
    long_description=LONG_DESCRIPTION,
    license='GPLv3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
       'certifi',
       'httplib2',
       'requests',
       'social-auth-core'
    ],
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: System Administrators',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 3 - Alpha',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 2.7',
    ]
)
