# vcf-report

[![Tests](https://github.com/CristiGuijarro/vcf-report/workflows/Test/badge.svg)](https://github.com/CristiGuijarro/vcf-report/actions?query=workflow%3ATest)

Python application to report metadata and other metrics from a VCF

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/CristiGuijarro/vcf-report.git
   ```

2. Navigate to the project directory:

    ```shell
    cd vcf-report
    ```

3. Install the dependencies and test dependencies:

    ```shell
    pip install -e '.[test]'
    ```

## Usage

For help, run:

    ```shell
    vcf-report --help
    ```

You can also use:

    ```shell
    python -m vcf_report --help
    ```

Running the application to generate a report with a VCF file:

    ```shell
    vcf-report report --vcf <path_to_vcf_file> [--out <path_to_output_file>]
    ```

Arguments:

`--vcf`: Path to the input VCF file. (Required)
`--out`: Path to the desired output report file. (Optional, default: vcf_report.json)
The application will parse the VCF file and generate a report with metadata and other metrics. The report will be saved in the specified output file.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    ```shell
    cd vcf-report
    python -m venv venv
    source venv/bin/activate
    ```

Now install the dependencies and test dependencies:

    ```shell
    pip install -e '.[test]'
    ```

To run the tests:

    ```shell
    pytest
    ```
