from io import BytesIO

from pypdf import PdfReader


class FileParsingService:
    def parse_file(self, filename: str, raw_content: bytes) -> str:
        normalized_filename = filename.lower()

        if normalized_filename.endswith((".txt", ".md")):
            return self._parse_text_file(raw_content)

        if normalized_filename.endswith(".pdf"):
            return self._parse_pdf_file(raw_content)

        raise ValueError("Unsupported file type")

    def _parse_text_file(self, raw_content: bytes) -> str:
        try:
            return raw_content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("File must be valid UTF-8 text") from error

    def _parse_pdf_file(self, raw_content: bytes) -> str:
        try:
            reader = PdfReader(BytesIO(raw_content))

            text_parts: list[str] = []

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text_parts.append(page_text)

            text = "\n\n".join(text_parts)

            if text.strip() == "":
                raise ValueError("Could not extract text from PDF")

            return text

        except ValueError:
            raise

        except Exception as error:
            raise ValueError("Failed to parse PDF file") from error


file_parsing_service = FileParsingService()