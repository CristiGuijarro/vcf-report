# vcf-report

[![PyPI](https://img.shields.io/pypi/v/vcf-report.svg)](https://pypi.org/project/vcf-report/)
[![Changelog](https://img.shields.io/github/v/release/CristiGuijarro/vcf-report?include_prereleases&label=changelog)](https://github.com/CristiGuijarro/vcf-report/releases)
[![Tests](https://github.com/CristiGuijarro/vcf-report/workflows/Test/badge.svg)](https://github.com/CristiGuijarro/vcf-report/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/CristiGuijarro/vcf-report/blob/master/LICENSE)

Python application to report metadata and other metrics from a VCF

## Installation

Install this tool using `pip`:

    pip install vcf-report

## Usage

For help, run:

    vcf-report --help

You can also use:

    python -m vcf_report --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd vcf-report
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
