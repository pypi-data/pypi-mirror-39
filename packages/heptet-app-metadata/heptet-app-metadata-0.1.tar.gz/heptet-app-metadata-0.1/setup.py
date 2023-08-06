from setuptools import setup, find_packages

requires = ['SqlAlchemy', 'plaster', 'plaster_pastedeploy', 'python-datauri']

packages = find_packages(exclude=['tests'])
print(packages)
setup(
    name='heptet-app-metadata',
    author='Kay Mccormick',
    author_email='kay@kaymccormick.com',
    version='0.1',
    packages=packages,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'heptet_db_dump = heptet_app_metadata.main:main',
        ],
    },
)
