from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

setup(
    name='azure-test-cli',
    version='0.4.1',
    packages=find_packages(),
    include_package_data=True,
    author="Michael Groves",
    author_email="mike@wildengineer.com",
    description="CLI to test azure resources, such as servicebus, eventhub, and storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wildengineer/azure-test-cli",
    install_requires=[
        'click',
        'asyncio',
        'azure-eventhub',
        'azure-servicebus',
        'azure-storage-blob'
    ],
    entry_points='''
        [console_scripts]
        aztest=azuretestcli.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
