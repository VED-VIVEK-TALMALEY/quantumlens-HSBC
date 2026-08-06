# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

class DocumentChunker:

    def chunk(
        self,
        pages,
        chunk_size=800,
        overlap=150
    ):

        chunks = []

        for page in pages:

            text = page["text"]

            start = 0

            while start < len(text):

                end = start + chunk_size

                chunk = text[start:end]

                chunks.append(
                    {
                        "text": chunk,
                        "page": page["page"],
                        "source": page["source"]
                    }
                )

                start += chunk_size - overlap

        return chunks