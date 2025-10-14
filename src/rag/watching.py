from chuncking import output



temp = output()
with open("/home/tarun/rag/data/output_5.txt", "w", encoding="utf-8") as f:
    for chunk in temp:
        f.write(chunk)
        # optionally ensure a newline if chunks don't already have one
        if not chunk.endswith('\n'):
            f.write('\n')

