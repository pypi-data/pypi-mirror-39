import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

packages = setuptools.find_packages()

setuptools.setup(
    name='hela-utils',
    version='0.3',
    author="Edward Brennan",
    author_email="ebrennan@redhat.com",
    description="Some luigi utility classes",
    long_description=long_description,
    url="https://gitlab.corp.redhat.com/mkt-ops-de/hela-utils.git",
    packages=packages,
    install_requires=["requests"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
