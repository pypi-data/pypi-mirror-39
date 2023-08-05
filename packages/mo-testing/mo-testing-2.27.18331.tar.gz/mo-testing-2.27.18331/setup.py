from setuptools import setup
setup(
    description="More Testing! Extends the `unittest.TestCase` to provide deep, yet fuzzy, structural comparisons",
    license="MPL 2.0",
    author="Kyle Lahnakoski",
    author_email="kyle@lahnakoski.com",
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)","Programming Language :: Python :: 3.6","Programming Language :: Python :: 2.7"],
    install_requires=["mo-collections>=1.2.18029","mo-dots>=2.20.18318","mo-future","mo-logs","mo-math>=1.2"],
    version="2.27.18331",
    url="https://github.com/klahnakoski/mo-testing",
    packages=["mo_testing"],
    long_description="Mo' Testing\r\n===========\r\n\r\n`FuzzyTestCase` extends the `unittest.TestCase` to provide deep, yet fuzzy, structural comparisons; intended for use in test cases dealing with JSON.\r\n\r\n\r\nDetails\r\n-------\r\n\r\nThe primary method is the `assertEqual` method with the following parameters:\r\n\r\n* `test_value` - the value, or structure being tested\r\n* `expected` - the expected value or structure.  In the case of a number, the accuracy is controlled by the following parameters.  In the case of a structure, only the not-null parameters of `expected` are tested for existence.\r\n* `msg` - Detailed error message if there is no match\r\n* `digits` - number of decimal places of accuracy required to consider two values equal\r\n* `places` - number of significant digits used to compare values for accuracy\r\n* `delta` - maximum difference between values for them to be equal\r\n\r\nThis method, `assertEqual` is recursive, so it does a deep comparison, and can not handle loops.\r\n\r\n\r\n",
    name="mo-testing"
)