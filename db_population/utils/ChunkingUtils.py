from tiktoken import get_encoding

CHUNK_SIZE = 400
OVERLAP_PERCENTAGE = 0.2

class ChunkingHelper:

    def __init__(self):
        self.enc = get_encoding("cl100k_base")

    def get_video_transcript_chunks(self, transcript) -> list[str]:
        tokens = self.enc.encode(transcript)
        chunks = []
        for i in range(0, len(tokens), CHUNK_SIZE-int(CHUNK_SIZE*OVERLAP_PERCENTAGE)):
            chunk = tokens[i:i+CHUNK_SIZE]
            chunks.append(self.enc.decode(chunk))
        return chunks