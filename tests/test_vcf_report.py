
import json
import shutil
from collections import Counter
from pathlib import Path

import pytest
from click.testing import CliRunner

from vcf_report.cli import cli
from vcf_report.vcf import VCFReport


@pytest.fixture
def vcf_report(tmp_path):
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

    Example:
        To use this fixture in a test:

        ```
        def test_vcf_report(vcf_report):
            # Test code
        ```
    """
    vcf_file = Path(__file__).resolve().parent / "testdata" / "chr20.variants_20072022.vcf"
    report_file = tmp_path / "test_report.json"

    shutil.copy2(str(vcf_file), str(tmp_path / vcf_file.name))

    return VCFReport(tmp_path / vcf_file.name)


def test_parse_vcf(vcf_report):
    vcf_report.parse_vcf()

    # Assert metadata
    assert vcf_report.metadata["num_samples"] == 3
    assert vcf_report.metadata["vcf_version"] == "VCFv4.3"
    assert vcf_report.metadata["vcf_format"] == "GT"

    # Assert variant information
    assert vcf_report.variant_info["snps"] == 7880
    assert vcf_report.variant_info["indels"] == 869
    assert dict(vcf_report.variant_info["substitution_types"]) == {
        "del": 495,
        "tv": 2332,
        "ins": 374,
        "ts": 5548
    }
    assert vcf_report.variant_info["heterozygous_variants"] == 10448
    assert vcf_report.variant_info["homozygous_variants"] == 15799
    assert dict(vcf_report.variant_info["variant_distribution"]) == {"20": 8749}
    assert dict(vcf_report.variant_info["mutational_processes"]) == {None: 8749}

def test_write_report(vcf_report, tmp_path):
    vcf_report.parse_vcf()  # Ensure that parse_vcf() is called before writing the report

    report_file = tmp_path / "report.json"
    vcf_report.write_report(report_file)

    # Read the report file and assert its content
    with open(report_file, mode="r", encoding="utf8") as file:
        report_data = json.load(file)

    expected_report_data={}
    expected_report_data["VCF Metadata"]={}
    expected_report_data["VCF Metadata"]["Number of samples"]=3
    expected_report_data["VCF Metadata"]["VCF version"]="VCFv4.3"
    expected_report_data["VCF Metadata"]["VCF format"]="GT"
    expected_report_data["Variant Information"]={}
    expected_report_data["Variant Information"]["Number of SNPs"]=7880
    expected_report_data["Variant Information"]["Number of indels"]=869
    expected_report_data["Variant Information"]["Substitution types"]={}
    expected_report_data["Variant Information"]["Substitution types"]["del"]=495
    expected_report_data["Variant Information"]["Substitution types"]["tv"]=2332
    expected_report_data["Variant Information"]["Substitution types"]["ins"]=374
    expected_report_data["Variant Information"]["Substitution types"]["ts"]=5548
    expected_report_data["Variant Information"]["Heterozygous variants"]=10448
    expected_report_data["Variant Information"]["Homozygous variants"]=15799
    expected_report_data["Variant Information"]["Variant distribution across chromosomes"]={}
    expected_report_data["Variant Information"]["Variant distribution across chromosomes"]["20"]=8749
    expected_report_data["Variant Information"]["Mutational processes"]={}
    expected_report_data["Variant Information"]["Mutational processes"]["null"]=8749

    assert report_data == expected_report_data


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")
