from setuptools import setup

setup(
    # to be displayed on PyPI
    name='klego',
    version='0.96.5',
    description='the beta v0.95 version of klego, an easy-to-go'
                ' python package for Lego NXT control'
                ' built especially for popular Lego tasks'
                ' like line-following and bonus block hitting',
    keywords='python lego nxt mindstorm easy',
    project_urls={
        'Documentation': 'https://github.com/KivenChen/PyLego',
        'Source Code': 'https://github.com/KivenChen/PyLego',
        'More by Kiven': "https://github.com/Kivenchen",
    },
    author='Kiven',
    author_email='sdckivenchen@gmail.com',
    url='https://kivenchen,us',

    packages=['klego'],
    install_requires=['pyusb', 'nxt-python', 'pybluez==0.22'],
    dependency_links=[
        'https://kivenchen.us/kiven-s-pybluez/PyBluez-0.22.tar.gz'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
