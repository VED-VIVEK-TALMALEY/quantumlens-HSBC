# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from pathlib import Path
import pdfplumber


class DocumentIngestion:

    def ingest(self, pdf_path: str):

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)

        pages = []

        with pdfplumber.open(pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                text = page.extract_text()

                if text is None:
                    continue

                text = text.strip()

                if not text:
                    continue

                pages.append(
                    {
                        "page": page_number,
                        "source": pdf_path.name,
                        "text": text
                    }
                )

        return pages


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    ingestion = DocumentIngestion()

    pages = ingestion.ingest(
        "data/HSBC_Q1_2026_Earnings_Release.pdf"
    )

    print(f"Pages extracted: {len(pages)}")

    print(pages[0])