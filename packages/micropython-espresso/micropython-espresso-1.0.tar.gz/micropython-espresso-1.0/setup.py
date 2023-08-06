from setuptools import setup

setup(
    name='micropython-espresso',
    version='1.0',
    packages=['espresso'],
    #package_dir = {'djangoforandroid': 'djangoforandroid'},

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    #url = 'http://www.pinguino.cc/',
    url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/micropythonespresso/micropython-espresso/downloads/',

    install_requires=['micropython-logging',

                      ],

    license='BSD License',
    description="A Micropython utils for.",
    #    long_description = README,

    classifiers=[
        # 'Environment :: Web Environment',
        # 'Framework :: Django',
    ],

)
