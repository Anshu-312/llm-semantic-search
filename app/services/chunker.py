def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50,
) -> list[str]:
    """Splits the input text into chunks of specified size with overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int, optional): The maximum size of each chunk. Defaults to 500.
        overlap (int, optional): The number of overlapping characters between chunks. Defaults to 50.

    Returns:
        list[str]: A list of text chunks.
    """
    words = text.split()
    chunks = []
    
    start = 0
    text_length = len(words)

    while start < text_length:
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start = end - overlap

    return chunks