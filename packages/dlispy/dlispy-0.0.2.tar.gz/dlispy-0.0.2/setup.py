import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlispy",
    version="0.0.2",
    description="A python library to parse DLIS file",
    long_description=long_description,
    platforms='any',
    test_suite='dlispy.tests.test_basic',
    long_description_content_type="text/markdown",
    url="https://github.com/teradata/dlispy",
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    license="BSD-3-Clause",
    install_requires=['atomicwrites==1.1.5',
                      'attrs==18.1.0',
                      'click==6.7',
                      'more-itertools==4.3.0',
                      'pluggy==0.7.1',
                      'py==1.5.4',
                      'pytest==3.7.1',
                      'six==1.11.0'
                     ],
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ]
)
