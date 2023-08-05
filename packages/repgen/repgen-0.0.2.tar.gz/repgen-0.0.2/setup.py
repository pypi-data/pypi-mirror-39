from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='repgen',
      version='0.0.2',
      description='A simple python REPort GENeration library',
      author='Libor Wagner',
      author_email='libor.wagner@cvut.cz',
      url='https://github.com/liborw/repgen',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['repgen'],
      install_requires=[
          'jinja2'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 2",
          "License :: OSI Approved :: MIT License",
      ]
)
