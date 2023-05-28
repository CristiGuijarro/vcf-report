"""Python class to report metadata, metrics and variant distribution from VCF"""
import json
from collections import Counter
from typing import List

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
        self.metadata["file_date"] = vcf_reader.metadata["fileDate"]
        self.metadata["source"] = vcf_reader.metadata["source"]
        self.metadata["reference_genome"] = vcf_reader.metadata["reference"]

        records = list(vcf_reader)  # Store the records in a list

        snps = 0
        indels = 0
        substitution_types = Counter()
        heterozygous_variants = 0
        homozygous_variants = 0

        for record in records:
            if record.is_snp:
                snps += 1
            elif record.is_indel:
                indels += 1

            substitution_types[record.var_subtype] += 1

            for sample in record.samples:
                if sample.is_het:
                    heterozygous_variants += 1
                else:
                    homozygous_variants += 1

        variant_distribution = chromosome_variant_distribution(records)
        mutational_processes = collect_mutational_processes(records, total_only=True)

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
        report_data = {
            "VCF Metadata": {
                "Number of samples": self.metadata["num_samples"],
                "VCF version": self.metadata["vcf_version"],
                "VCF format": self.metadata["vcf_format"],
                "File Date": self.metadata["file_date"],
                "Data Source": self.metadata["source"],
                "Reference Genome": self.metadata["reference_genome"],
            },
            "Variant Information": {
                "Number of SNPs": self.variant_info["snps"],
                "Number of indels": self.variant_info["indels"],
                "Substitution types": dict(self.variant_info["substitution_types"]),
                "Heterozygous variants": self.variant_info["heterozygous_variants"],
                "Homozygous variants": self.variant_info["homozygous_variants"],
                "Variant distribution across chromosomes": dict(
                    self.variant_info["variant_distribution"]
                ),
                "Mutational processes": dict(self.variant_info["mutational_processes"]),
            },
        }
        with open(report_file, mode="w", encoding="utf8") as report:
            json.dump(report_data, report, indent=4)


def chromosome_variant_distribution(records: list) -> dict:
    """Calculates the variant distribution across chromosomes from a list of records.

    This function analyzes the variants in a list of VCF records and counts the number
    of variants present on each chromosome, providing the variant distribution
    information.

    Args:
        records (list): A list of VCF records.

    Returns:
        dict: A dictionary containing the variant distribution across chromosomes.
              The keys are chromosome names, and the values are the corresponding
              counts of variants for each chromosome.
    """
    chromosome_counts = {}

    for record in records:
        chromosome = record.CHROM
        chromosome_counts.setdefault(chromosome, 0)
        chromosome_counts[chromosome] += 1

    return chromosome_counts


def collect_mutational_processes(records: list, total_only=False) -> dict:
    """Collects the mutational processes from a list of records.

    This function analyzes the substitution types of the variants in a list of VCF records
    to generate possible mutational processes.

    Args:
        records (list): A list of VCF records.
        total_only (bool): If true returns the total frequency of possible mutational
                           processes.

    Returns:
        dict: A dictionary containing the mutational processes and their frequencies,
              sorted by frequency in descending order.
    """

    substitution_dict = {}

    for record in records:
        ref_allele = record.REF
        alt_alleles = record.ALT

        # Calculate the substitution type for each ALT allele
        for alt_allele in alt_alleles:
            substitution = ref_allele + ">" + str(alt_allele)
            substitution_dict.setdefault(substitution, 0)
            substitution_dict[substitution] += 1

    sorted_dict = dict(
        sorted(substitution_dict.items(), key=lambda item: item[1], reverse=True)
    )
    total_processes = len(sorted_dict.keys())
    if total_only:
        total_processes_dict = {"Total Processes": total_processes}
        return total_processes_dict

    sorted_dict["Total Processes"] = total_processes
    return sorted_dict
