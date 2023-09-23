#!/usr/bin/env python3

import pypdf


def merge_pdfs(output_file, input_files):
    pdf_merger = pypdf.PdfMerger()

    for input_file in input_files:
        try:
            pdf_merger.append(input_file)
        except pypdf.utils.PdfReadError:
            print(f"Error loading file: {input_file}")

    with open(output_file, "wb") as output_pdf:
        pdf_merger.write(output_pdf)

    print(f"PDF files merged successfully! Output file: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Merges PDF files.")
    parser.add_argument("output_file", help="Output PDF file")
    parser.add_argument("input_files", nargs="+", help="Input PDF files")
    args = parser.parse_args()

    merge_pdfs(args.output_file, args.input_files)
