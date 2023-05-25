"""Python class to report metadata, metrics and variant distribution from VCF"""
from collections import Counter

import vcf

class VCFReport:
    """
    Represents a VCF (Variant Call Format) file and provides methods to
    parse the file and generate a report.
    """

    def __init__(self, vcf_file):
        """
        Initialize the VCF object with the path to the VCF file.

        Args:
            vcf_file (str): Path to the VCF file.
        """
        self.vcf_file = vcf_file
        self.metadata = {}
        self.variant_info = {}

    def parse_vcf(self):
        """
        Parse the VCF file and extract general metadata and variant information.
        """
        vcf_reader = vcf.Reader(open(self.vcf_file, mode="r", encoding="utf8"))

        self.metadata["num_samples"] = len(vcf_reader.samples)
        self.metadata["vcf_version"] = vcf_reader.metadata["fileformat"]
        self.metadata["vcf_format"] = ", ".join(vcf_reader.formats.keys())

        snps = 0
        indels = 0
        substitution_types = Counter()
        heterozygous_variants = 0
        homozygous_variants = 0
        variant_distribution = Counter()
        mutational_processes = Counter()

        for record in vcf_reader:
            if record.is_snp:
                snps += 1
            elif record.is_indel:
                indels += 1

            substitution_types[record.var_subtype] += 1

            for sample in record.samples:
                if sample.is_het:
                    heterozygous_variants += 1
                elif sample.is_hom:
                    homozygous_variants += 1

            variant_distribution[record.CHROM] += 1
            mutational_processes[record.INFO.get("MUT_PROCESS")] += 1

        self.variant_info["snps"] = snps
        self.variant_info["indels"] = indels
        self.variant_info["substitution_types"] = substitution_types
        self.variant_info["heterozygous_variants"] = heterozygous_variants
        self.variant_info["homozygous_variants"] = homozygous_variants
        self.variant_info["variant_distribution"] = variant_distribution
        self.variant_info["mutational_processes"] = mutational_processes

    def write_report(self, report_file):
        """
        Write a report with the parsed VCF metadata and variant information.

        Args:
            report_file (str): Path to the report file.
        """
        with open(report_file, mode="w", encoding="utf8") as report:
            report.write("VCF Metadata:\n")
            report.write(f"Number of samples: {self.metadata['num_samples']}\n")
            report.write(f"VCF version: {self.metadata['vcf_version']}\n")
            report.write(f"VCF format: {self.metadata['vcf_format']}\n\n")

            report.write("Variant Information:\n")
            report.write(f"Number of SNPs: {self.variant_info['snps']}\n")
            report.write(f"Number of indels: {self.variant_info['indels']}\n")
            report.write(
                f"Substitution types: {self.variant_info['substitution_types']}\n"
            )
            report.write(
                f"Heterozygous variants: {self.variant_info['heterozygous_variants']}\n"
            )
            report.write(
                f"Homozygous variants: {self.variant_info['homozygous_variants']}\n"
            )
            report.write(
                f"Variant distribution across chromosomes: {self.variant_info['variant_distribution']}\n"
            )
            report.write(
                f"Mutational processes: {self.variant_info['mutational_processes']}\n"
            )
