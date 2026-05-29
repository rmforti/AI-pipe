from uuid import UUID, uuid4

from app.models.chunk import Chunk


class ChunkingService:
    def chunk_text(
        self,
        document_id: UUID,
        text: str,
        chunk_size: int = 500,
    ) -> list[Chunk]:
        chunks: list[Chunk] = []
        chunk_index = 0

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        current_chunk = ""

        for paragraph in paragraphs:
            if len(paragraph) > chunk_size:
                if current_chunk:
                    chunks.append(
                        Chunk(
                            id=uuid4(),
                            document_id=document_id,
                            text=current_chunk,
                            chunk_index=chunk_index,
                        )
                    )
                    chunk_index += 1
                    current_chunk = ""

                for chunk_text in self._split_large_paragraph(
                    paragraph=paragraph,
                    chunk_size=chunk_size,
                ):
                    chunks.append(
                        Chunk(
                            id=uuid4(),
                            document_id=document_id,
                            text=chunk_text,
                            chunk_index=chunk_index,
                        )
                    )
                    chunk_index += 1

                continue

            separator_length = 2 if current_chunk else 0

            if len(current_chunk) + separator_length + len(paragraph) <= chunk_size:
                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph
            else:
                if current_chunk:
                    chunks.append(
                        Chunk(
                            id=uuid4(),
                            document_id=document_id,
                            text=current_chunk,
                            chunk_index=chunk_index,
                        )
                    )
                    chunk_index += 1

                current_chunk = paragraph

        if current_chunk:
            chunks.append(
                Chunk(
                    id=uuid4(),
                    document_id=document_id,
                    text=current_chunk,
                    chunk_index=chunk_index,
                )
            )

        return chunks

    def _split_large_paragraph(
        self,
        paragraph: str,
        chunk_size: int,
    ) -> list[str]:
        sentences = paragraph.split(". ")

        chunks: list[str] = []
        current_chunk = ""

        for sentence in sentences:
            if not sentence.endswith("."):
                sentence += "."

            separator = " " if current_chunk else ""

            if len(current_chunk) + len(separator) + len(sentence) <= chunk_size:
                current_chunk += separator + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)

                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks


chunking_service = ChunkingService()