from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), "r") as fh:
    long_description = fh.read()

setup(
    name="WebNMS",
    version="1.b1",
    author="WebNMS",
    author_email="webnms-edge@zohocorp.com",
    description="A package providing provisions for connecting with a WebNMS IoT platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.webnms.com/",
    packages=find_packages(),
    data_files = [("", ["LICENSE.txt"])],
    classifiers=[
	'Development Status :: 4 - Beta',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    keywords='IoT sensors',
    python_requires='>=2.7',
    install_requires=[
        "requests",
   ]
)
