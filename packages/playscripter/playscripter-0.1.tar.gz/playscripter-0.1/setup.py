from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

setup(
    name='playscripter',
    version='0.1',
    packages=['scripter'],
    url='https://github.com/NCPlayz/Scripter',
    license='MIT',
    author='NCPlayz <Nadir Chowdhury>',
    author_email='chowdhurynadir0@outlook.com',
    description='A Python alternative to making playscripts.',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=requirements,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
