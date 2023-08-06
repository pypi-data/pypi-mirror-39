from setuptools import setup

setup(

    name="web_assist",
    version='0.0.5',
    url='https://github.com/pytholabsbot1/web-assist',
    author='Pytholabs',
    author_email='info@pytholabs.com',  
    description='Tools for scraping and downloading internet resources',
    py_modules=['webAssist'],
    package_dir={'':'src'},

    install_requires=[
          'requests',
      ],

    )
