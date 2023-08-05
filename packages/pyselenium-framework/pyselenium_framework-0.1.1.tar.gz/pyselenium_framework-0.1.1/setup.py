from setuptools import setup, find_packages
version = '0.1.1'

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='pyselenium_framework',
    version=version,
    packages=find_packages(exclude=['AUT', 'Execution']),
    author=u'Wally Yu',
    install_requires=['selenium==3.14.1'],
    url='https://github.com/wally-yu/selenium-framework',
    include_package_data=True,
    license='MIT License',
    description='A Python Selenium Framework Which Makes Code More Easy to Maintain and Read',
    long_description=long_description,
    long_description_content_type='text/markdown',
      )
