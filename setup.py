from setuptools import setup, find_packages

setup(
    name="dance_scheduler",
    version="0.1.0",
    description="A tool for optimizing dance schedules",
    author="Kai Arseneau",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "networkx"
    ],
    entry_points={
        "console_scripts": [
            "dance_scheduler = dance_scheduler.main:main"
        ]
    }
)