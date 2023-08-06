from setuptools import setup, Extension
from Cython.Build import cythonize


with open("README.md", "r") as file:
    long_description = file.read()

setup(
    ext_modules=cythonize(
        Extension(
            name="Fortuna",
            sources=["Fortuna.pyx"],
            language=["c++"],
            extra_compile_args=["-std=c++17"],
        ),
        compiler_directives={
            'embedsignature': True,
            'language_level': 3,
        },
    ),
    name="Fortuna",
    author="Broken aka Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    url="https://sharpdesigndigital.com",
    requires=["Cython"],
    version="0.20.7",
    description="Fast & Flexible Random Value Generators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["fortuna_extras"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        'Development Status :: 4 - Beta',
    ],
    keywords=[
        "Fortuna", "Random Patterns", "Data Perturbation", "Game Dice", "Weighted Choice", "Random Cycle",
        "Random Value", "Gaussian Distribution", "Linear Geometric Distribution", "Truffle Shuffle", "FlexCat",
        "Percent True", "Zero Cool", "Quantum Monty", "Custom Distribution", "Rarity Table"
    ],
    python_requires='>=3.6',
)
