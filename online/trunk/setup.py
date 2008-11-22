try:
    from setuptools import setup, find_packages
except ImportError:
    print 'Please install setuptools'
    import sys
    sys.exit(-1)

setup(
    name='WebGriffith',
    version='0.1~dev',
    description='',
    author='Piotr Ożarowski',
    author_email='piotr@griffith.cc',
    url='http://online.griffith.cc',
    install_requires=[
        "Pylons>=0.9.7rc3",
        "SQLAlchemy>=0.5rc4",
        "Mako>=0.2.2",
        "Beaker",
        "Webhelpers",
    ],
    setup_requires=["PasteScript==dev,>=1.6.3dev-r7326"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'webgriffith': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'webgriffith': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = webgriffith.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
