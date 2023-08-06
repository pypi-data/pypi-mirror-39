import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rolling_window',
    version='0.1',
    packages=setuptools.find_packages(),
    license='MIT License',
    long_description=long_description,
    install_requires=['hickle','paco','numpy'],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)