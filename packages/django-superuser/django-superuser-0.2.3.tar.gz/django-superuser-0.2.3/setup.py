from setuptools import setup


setup(
    name='django-superuser',
    version='0.2.3',
    description='Middleware that gives you super powers.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    author='Mikko Hellsing',
    author_email='mikko@sumusm.se',
    url='http://github.com/sorl/django-superuser',
    packages=['superuser'],
    zip_safe=False,
    license='ICS',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
    ],
)
