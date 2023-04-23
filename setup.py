"""
nba_player_performance_prediction

A project to predict NBA player performance
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nba_player_performance_prediction",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A project to predict NBA player performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asap-blocky/nba-player-performance-prediction-model",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "numpy",
        "requests",
        "beautifulsoup4",
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "nba-player-prediction=nba_player_performance_prediction.main:main",
        ],
    },
)
