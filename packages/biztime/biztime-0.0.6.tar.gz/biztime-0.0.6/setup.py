import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="biztime",
  version="0.0.6",
  author="austen0",
  author_email="austen@cas3y.com",
  description=("Utility for calculating the total working time between given "
               "dates/times."),
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/austen0/biztime",
  packages=setuptools.find_packages(exclude=["tests"]),
)
