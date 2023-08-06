import setuptools

setuptools.setup(
    name="bay_adder",
    version="0.0.1",
    author="Alex Bers",
    author_email="bay@hackerdom.ru",
    description="Adds two nums",
    long_description="Long description",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    py_modules = ['bay_adder'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
