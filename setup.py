from setuptools import setup, find_packages

version = '0.3'

setup(
    name='finch-cms',
    version=version,
    description="Simple but flexible CMS for django",
    long_description=open('README.rst').read(),
    keywords='django cms',
    author='Peter van Kampen',
    author_email='pterk@datatailors.com',
    url='https://github.com/pterk/finch-cms',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django==1.3',
        'PIL==1.1.7',
        'South==0.7.3',
        'Whoosh==2.3.0',
        'django-bop==0.3',
        'django-filebrowser==3.3.0',
        'django-grappelli==2.3.5',
        'django-haystack==1.2.5',
        'django-treebeard==1.61',
        'django-contentmanager==11.10.1',
        'django-tinymce'
        ],
    dependency_links = [
        'https://github.com/aljosa/django-tinymce.git#egg=django-tinymce'
        ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
