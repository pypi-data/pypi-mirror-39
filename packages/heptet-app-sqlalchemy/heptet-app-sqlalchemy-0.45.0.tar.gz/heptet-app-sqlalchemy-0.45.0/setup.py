from setuptools import setup, find_packages

requires = [
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_tm',
    'pyramid_retry',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='heptet-app-sqlalchemy',
    version='0.45.0',
    description='Heptet App SQLAlchemy component',
    long_description='Heptet App SQLAlchemy component',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Kay McCormick',
    author_email='kay@kaymccormick.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'console_scripts': [
        ],
    },
)

