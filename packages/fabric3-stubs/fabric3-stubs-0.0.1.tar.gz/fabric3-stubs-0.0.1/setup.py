from setuptools import setup

setup(
    name="fabric3-stubs",
    version="0.0.1",
    packages=["fabric3-stubs"],
    package_data={
        "fabric3-stubs": ["*.pyi"],
    },
    install_requires=[
        "fabric3==1.14.post1",
    ],
)

