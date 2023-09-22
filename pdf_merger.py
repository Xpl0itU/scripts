#!/usr/bin/env python3

import sys
import pypdf


def merge_pdfs(output_file, input_files):
    pdf_merger = pypdf.PdfFileMerger()

    for input_file in input_files:
        try:
            pdf_merger.append(input_file)
        except pypdf.utils.PdfReadError:
            print(f"Error loading file: {input_file}")

    with open(output_file, "wb") as output_pdf:
        pdf_merger.write(output_pdf)

    print(f"PDF files merged successfully! Output file: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pdf_merger.py output.pdf input1.pdf input2.pdf ...")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]

    merge_pdfs(output_file, input_files)
