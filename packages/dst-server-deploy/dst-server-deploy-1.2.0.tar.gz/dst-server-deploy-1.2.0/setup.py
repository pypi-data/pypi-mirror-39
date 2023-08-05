#from distutils.core import setup
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='dst-server-deploy',
      version='1.2.0',
      description="Generate files to deploy a Don't Starve Together Server Docker Container.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment :: Role-Playing',
      ],
      keywords='DST dont starve together server docker docker-compose',
      url='https://gitlab.com/lego_engineer/dst-server-deploy',
      author='lego_engineer',
      author_email='protopeters@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['PyYAML>=3.13'],
      python_requires='>=3.5',
      scripts=['dst_server_deploy/bin/dst-server-deploy']
      )
