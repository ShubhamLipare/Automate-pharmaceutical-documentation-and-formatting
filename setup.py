from setuptools import setup, find_packages

setup(
    name="ai-owners-manual",
    version="0.1.0",
    description="Automate pharmaceutical documentation and formatting",
    author="Shubham",
    packages=find_packages(exclude=("notebook", "logs", ".venv")),
    python_requires=">=3.10",
)