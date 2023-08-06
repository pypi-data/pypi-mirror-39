import setuptools

long_description = """\
`biztime` is a is a utility for calculating the total time between given
dates/times, while omitting non-working hours, weekends, and holidays as
configured by the user. Includes additional helper functions for interacting
with various `datetime` objects.

See the [GitHub project](https://github.com/austen0/biztime) for usage examples
and a syntax reference.
"""

setuptools.setup(
  name="biztime",
  version="0.0.8",
  author="austen0",
  author_email="austen@cas3y.com",
  description=("Utility for calculating the total working time between given "
               "dates/times."),
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/austen0/biztime",
  packages=setuptools.find_packages(exclude=["tests"]),
)
