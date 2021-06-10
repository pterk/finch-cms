from setuptools import setup, find_packages

from finch import __version__

setup(
    name='finch-cms',
    version=__version__,
    description="Simple but flexible CMS for django",
    long_description=open('README.rst').read(),
    keywords='django cms',
    author='Peter van Kampen',
    author_email='pterk@datatailors.com',
    url='https://github.com/pterk/finch-cms',
    license='BSD',
    packages=find_packages(),
    #package_data={'finch': ['templates/*/*',
    #                        'static/*/*/*/*/*/*/*/*/*',
    #                        ]},
    include_package_data=True,
    install_requires=[
        'Django==2.2.24',
        'pillow',
        'South',
        'Whoosh',
        'django-bop',
        'django-filebrowser',
        #'django-grappelli==2.3.5',
        'django-haystack',
        'django-treebeard',
        'django-contentmanager',
        'django-tinymce'
        ],
    dependency_links = [
        'https://github.com/aljosa/django-tinymce/tarball/master#egg=django-tinymce-trunk'
        ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
