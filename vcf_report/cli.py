import click

from vcf_report.vcf import VCFReport


@click.group()
@click.version_option()
def cli():
    "Python application to report metadata and other metrics from a VCF"


@cli.command(name="report")
@click.argument("vcf")
@click.option("--vcf", help="Path to vcf file", required=True)
@click.option("--out", help="Path to desired output file", default="vcf_report.txt")
def report_vcf(vcf: str, out: str) -> None:
    """Runs the VCFReport `class` functions to write report
    \f
    Args:
        vcf (str): path to input vcf file
        out (str): path to output report file
    """
    vcf_file = vcf
    report_file = "path/to/report.txt"

    vcf_obj = VCFReport(vcf_file)
    vcf_obj.parse_vcf()
    vcf_obj.write_report(report_file)


if __name__ == "__main__":
    cli()
