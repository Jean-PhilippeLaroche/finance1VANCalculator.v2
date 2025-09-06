import pdfplumber
from pathlib import Path
from PIL import ImageOps
import pytesseract

def pdf_to_text(pdf_path: str) -> str:
    """
    Extract text from a PDF using pdfplumber
    :param pdf_path: Path to pdf file
    :return: Concatenated text for all pages
    """
    text_parts = []

    # opening pdf with pdfplumber, using with so file closes
    with pdfplumber.open(pdf_path) as pdf:

        # extracting text from each page of each pdf
        for page in pdf.pages:
            page_text = page.extract_text()
            # adding text in text_parts only if text was found in pdf
            if page_text:
                text_parts.append(page_text)

    # joins all text in a single string separated by \n
    return "\n".join(text_parts)


def pdf_to_text_with_ocr(pdf_path: str) -> str:
    """
    Extract text and image_text in scanned pdf documents
    :param pdf_path: Path to pdf file
    :return: Concatenated text for all pages
    """
    text_parts = []

    # opening pdf with pdfplumber, using with so file closes
    with pdfplumber.open(pdf_path) as pdf:

        # extracting text from each page of each pdf
        for page in pdf.pages:
            text = page.extract_text()
            # adding text in text_parts only if text was found in pdf
            if text:
                text_parts.append(text)

            else:
                # render page to an image, then convert the image to text
                im = page.to_image(resolution=300).original

                # convert to grayscale
                im = im.convert("L")

                # increase contrast (makes text stand out)
                im = ImageOps.autocontrast(im)

                # OCR, tries french first then english if needed
                ocr_text = pytesseract.image_to_string(im, lang="fra+eng")
                text_parts.append(ocr_text)

    # joins all text in a single string separated by \n
    return "\n".join(text_parts)




#def save_text_to_file(pdf_path: str, output_dir: str = "data/texts"):
#    """Extract text from a PDF and save it as a .txt file."""
#    pdf_path = Path(pdf_path)
#    output_dir = Path(output_dir)
#    output_dir.mkdir(parents=True, exist_ok=True)

#    text = pdf_to_text_with_ocr(pdf_path)
#    txt_filename = output_dir / f"{pdf_path.stem}.txt"

#    with open(txt_filename, "w", encoding="utf-8") as f:
#        f.write(text)

#    print(f"Saved text from {pdf_path.name} to {txt_filename}")




if __name__ == "__main__":

    # accessing the directory
    samples_dir = Path(__file__).resolve(). parents[1] / "data" / "samples"

    # accessing each pdf, printing its name then converting the pdf object to a str
    for pdf in samples_dir.glob("*.pdf"):
        print(f"\n==== {pdf.name} ====")
        txt = pdf_to_text(str(pdf))

        # assuming pdf has no texts if nothing was stripped
        if not txt.strip():
            print("[No text found]")
        else:
            print(txt)