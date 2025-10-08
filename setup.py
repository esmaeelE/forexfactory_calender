from setuptools import setup, find_packages

setup(
    name="forexfactory-scraper",
    version="0.1.0",
    author="Abolfazl Abbasi",
    author_email="a.abbasi5775@gmail.com",
    description="A Python package to fetch and parse Forex Factory events with filtering and scheduling capabilities.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abbasi0abolfazl/forexfactory-scraper",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.32.3",
        "click>=8.0.0",
        "schedule>=1.2.2",
        "pytz>=2025.1",
        "tzlocal>=5.3.1",
    ],
    extras_require={
    "dev": ["pytest>=7.0", "mypy>=0.900", "sphinx>=5.0", "sphinx-rtd-theme>=1.0", "sphinx-autodoc-typehints>=1.19"],
    },
    entry_points={
        "console_scripts": [
            "forexfactory-scraper=forexfactory_scraper.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",  
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)