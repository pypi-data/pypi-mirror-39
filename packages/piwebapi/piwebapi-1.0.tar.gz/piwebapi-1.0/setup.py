from setuptools import setup

setup(name='piwebapi',
      version='1.0',
      description='Vitens PI Wrapper',
      url='https://github.com/AbelHeinsbroek/piwebapi',
      author='Abel Heinsbroek',
      author_email='abel.heinsbroek@vitens.nl',
      license='Apache Licence 2.0',
      packages=['piwebapi'],
      install_requires=[
          'pandas'
      ],
      zip_safe=False)
