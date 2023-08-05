from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ovc',
      version='0.1.3',
      description='SDK for ansible modules used by GiG for their OpenVCloud platform',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Stef Graces',
      license='Nubera BVBA',
      packages=setuptools.find_packages(),
       classifiers=[
        "Operating System :: OS Independent",
    ],)