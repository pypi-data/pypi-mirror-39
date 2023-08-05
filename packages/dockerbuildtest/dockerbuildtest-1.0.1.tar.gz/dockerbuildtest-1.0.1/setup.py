import setuptools 
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


# specify requirements of your package here
REQUIREMENTS = [
    'docker',
    'Flask_RESTful',
    'Flask',
    'jsonschema',
    'pydash'
]

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5'
]

setuptools.setup(
    name="dockerbuildtest",
    version="1.0.1",
    author="Suresh Thumma",
    author_email="suresh@stackaero.com",
    description="docker build engine provide flaxibilty to build docker images",
    long_description=long_description,
    url="https://git.stackaero.com/stackengine/dockerbuildagent",
    license='MIT',
    download_url="https://git.stackaero.com/stackengine/dockerbuildagent",
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    include_package_data=True,
    keywords='python3 -m dockerbuildagent',
    zip_safe=False
)























# import setuptools 
# from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()


# # specify requirements of your package here
# REQUIREMENTS = [
#     'docker',
#     'Flask_RESTful',
#     'Flask',
#     'jsonschema',
#     'pydash'
# ]

# # some more details
# CLASSIFIERS = [
#     'Development Status :: 4 - Beta',
#     'Intended Audience :: Developers',
#     'Topic :: Software Development :: Build Tools',
#     'License :: OSI Approved :: MIT License',
#     'Programming Language :: Python :: 3',
#     'Programming Language :: Python :: 3.3',
#     'Programming Language :: Python :: 3.4',
#     'Programming Language :: Python :: 3.5'
# ]

# setuptools.setup(
#     name="dockerbuildagent",
#     version="1.0.2",
#     author="Suresh Thumma",
#     author_email="suresh@stackaero.com",
#     description="docker build engine provide flaxibilty to build docker images",
#     long_description=long_description,
#     url="https://git.stackaero.com/stackengine/dockerbuildagent",
#     license='MIT',
#     download_url="https://git.stackaero.com/stackengine/dockerbuildagent",
#     packages=find_packages(),
#     classifiers=CLASSIFIERS,
#     install_requires=REQUIREMENTS,
#     include_package_data=True,
#     keywords='python3 -m dockerbuildagent',
#     zip_safe=False
# )
