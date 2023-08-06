from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='delayed_assert',
    version='0.2',
    description='Delayed/soft assertions for python',
    long_description = long_description,
    author='pr4bh4sh',
    url='https://github.com/pr4bh4sh/python-delayed-assert',
    packages=['delayed_assert'],
)
