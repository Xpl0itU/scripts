#!/usr/bin/env python3

import os
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Inches, Mm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.xmlchemy import OxmlElement
from docx.oxml.shared import qn


def add_toc(doc):
    toc_heading = doc.add_heading("Table Of Contents", level=0)
    toc_heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    paragraph = doc.add_paragraph()
    run = paragraph.add_run()

    fldChar = OxmlElement("w:fldChar")
    fldChar.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = 'TOC \\f \\o "1-9" \\h'

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")

    fldChar3 = OxmlElement("w:t")
    fldChar3.text = "Right-click to update field."

    fldChar4 = OxmlElement("w:fldChar")
    fldChar4.set(qn("w:fldCharType"), "end")

    r_element = run._r
    r_element.append(fldChar)
    r_element.append(instrText)
    r_element.append(fldChar2)
    r_element.append(fldChar3)
    r_element.append(fldChar4)

    doc.add_paragraph()


def add_borders(doc):
    sec_pr = doc.sections[0]._sectPr
    pg_borders = OxmlElement("w:pgBorders")
    pg_borders.set(qn("w:offsetFrom"), "page")
    for border_name in ("left", "right"):
        border_el = OxmlElement(f"w:{border_name}")
        border_el.set(qn("w:val"), "single")
        border_el.set(qn("w:sz"), "4")
        border_el.set(qn("w:space"), "24")
        border_el.set(qn("w:color"), "auto")
        pg_borders.append(border_el)
    for border_name in ("top", "bottom"):
        border_el = OxmlElement(f"w:{border_name}")
        border_el.set(qn("w:val"), "single")
        border_el.set(qn("w:sz"), "4")
        border_el.set(qn("w:space"), "0")
        border_el.set(qn("w:color"), "auto")
        pg_borders.append(border_el)
    sec_pr.append(pg_borders)


def create_document():
    doc = Document()

    current_section = doc.sections[-1]
    # Set format to A4
    current_section.page_height = Mm(297)
    current_section.page_width = Mm(210)
    # Rotate to landscape
    new_width, new_height = current_section.page_height, current_section.page_width
    current_section.orientation = WD_ORIENT.LANDSCAPE
    current_section.page_width = new_width
    current_section.page_height = new_height

    title_heading = doc.add_heading("Title", level=0)
    title_heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_page_break()

    # Add empty page for table of contents
    add_toc(doc)
    doc.add_page_break()

    return doc


def add_images_to_document(doc, screenshot_folder):
    image_files = [
        f
        for f in os.listdir(screenshot_folder)
        if f.endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

    for image_file in image_files:
        image_path = os.path.join(screenshot_folder, image_file)
        doc.add_heading(image_file, level=1)
        doc.add_picture(image_path, width=Inches(6))
        doc.add_page_break()


def format_sections(doc):
    for section in doc.sections:
        section.top_margin = Inches(0)
        section.bottom_margin = Inches(0)
        section.left_margin = Inches(0.2)
        section.right_margin = Inches(0.2)


def main(output_docx, screenshot_folder):
    doc = create_document()
    add_images_to_document(doc, screenshot_folder)
    format_sections(doc)
    add_borders(doc)
    doc.save(output_docx)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a Word document with images.")
    parser.add_argument("output_docx", help="Output document filename")
    parser.add_argument("screenshot_folder", help="Folder containing image files")
    args = parser.parse_args()

    main(args.output_docx, args.screenshot_folder)
