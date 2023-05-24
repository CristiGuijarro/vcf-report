from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="vcf-report",
    description="Python application to report metadata and other metrics from a VCF",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Cristina Guijarro-Clarke",
    url="https://github.com/CristiGuijarro/vcf-report",
    project_urls={
        "Issues": "https://github.com/CristiGuijarro/vcf-report/issues",
        "CI": "https://github.com/CristiGuijarro/vcf-report/actions",
        "Changelog": "https://github.com/CristiGuijarro/vcf-report/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["vcf_report"],
    entry_points="""
        [console_scripts]
        vcf-report=vcf_report.cli:cli
    """,
    install_requires=["click", "PyVCF3"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
