import json
import shutil
from collections import Counter
from pathlib import Path

import pytest
from click.testing import CliRunner

from vcf_report.cli import cli
from vcf_report.vcf import VCFReport


@pytest.fixture
def vcf_report(tmp_path: Path) -> None:
    """
    Fixture for generating a VCFReport object for testing.

    This fixture creates a temporary directory and copies the VCF file
    "chr20.variants_20072022.vcf" from the "testdata" directory into the
    temporary directory. It then initializes a VCFReport object using the
    copied VCF file.

    Args:
        tmp_path (py.path.local): Temporary directory provided by pytest.

    Returns:
        VCFReport: VCFReport object initialized with the copied VCF file.

    Raises:
        FileNotFoundError: If the VCF file "chr20.variants_20072022.vcf" is
        not found in the "testdata" directory.
        ```
    """
    vcf_file = (
        Path(__file__).resolve().parent / "testdata" / "chr20.variants_20072022.vcf"
    )
    report_file = tmp_path / "test_report.json"

    shutil.copy2(str(vcf_file), str(tmp_path / vcf_file.name))

    return VCFReport(tmp_path / vcf_file.name)


def test_parse_vcf(vcf_report: VCFReport) -> None:
    """
    Test the parsing of a VCF file using the `parse_vcf()` method of a `VCFReport` object.

    Args:
        vcf_report (VCFReport): An instance of the `VCFReport` class.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    vcf_report.parse_vcf()

    # Assert metadata
    assert vcf_report.metadata["num_samples"] == 3
    assert vcf_report.metadata["vcf_version"] == "VCFv4.3"
    assert vcf_report.metadata["vcf_format"] == "GT"
    assert vcf_report.metadata["file_date"] == "26022019_15h52m43s"

    # Assert variant information
    assert vcf_report.variant_info["snps"] == 7880
    assert vcf_report.variant_info["indels"] == 869
    assert dict(vcf_report.variant_info["substitution_types"]) == {
        "del": 495,
        "tv": 2332,
        "ins": 374,
        "ts": 5548,
    }
    assert vcf_report.variant_info["heterozygous_variants"] == 10448
    assert vcf_report.variant_info["homozygous_variants"] == 15799
    assert dict(vcf_report.variant_info["variant_distribution"]) == {"20": 8749}
    assert dict(vcf_report.variant_info["mutational_processes"]) == {"Total Processes": 324}


def test_write_report(vcf_report: VCFReport, tmp_path: Path) -> None:
    """
    Test the writing of a report file using the `write_report()` method of a `VCFReport` object.

    Args:
        vcf_report (VCFReport): An instance of the `VCFReport` class.
        tmp_path (pathlib.Path): Temporary directory path for creating the report file.

    Raises:
        AssertionError: If the generated report data does not match the expected report data.
    """
    vcf_report.parse_vcf()

    report_file = tmp_path / "report.json"
    vcf_report.write_report(report_file)

    with open(report_file, mode="r", encoding="utf8") as file:
        report_data = json.load(file)

    expected_report_json = """
    {
        "VCF Metadata": {
            "Number of samples": 3,
            "VCF version": "VCFv4.3",
            "VCF format": "GT",
            "File Date": "26022019_15h52m43s",
            "Data Source": [
                "IGSRpipeline"
            ],
            "Reference Genome": "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa"
        },
        "Variant Information": {
            "Number of SNPs": 7880,
            "Number of indels": 869,
            "Substitution types": {
                "del": 495,
                "tv": 2332,
                "ins": 374,
                "ts": 5548
            },
            "Heterozygous variants": 10448,
            "Homozygous variants": 15799,
            "Variant distribution across chromosomes": {
                "20": 8749
            },
            "Mutational processes": {
                "Total Processes": 324
            }
        }
    }
    """
    expected_report_data = json.loads(expected_report_json)

    assert report_data == expected_report_data


def test_version():
    """Test the CLI version command.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")
