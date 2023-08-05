
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='address2img',
     version='1.1',
     scripts=['map_maker.py'] ,
     author="Martin Miglio",
     author_email="marmig0404@gmail.com",
     description="A module to convert addresses to images using mapnik",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/marmig0404/address2img",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 2.7",
     ],
 )