def get_binary_file_stream(file_path: str, chunk_bytes: int = 100):
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_bytes)
            if chunk:
                yield chunk
            else:
                break
