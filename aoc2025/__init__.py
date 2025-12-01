def load_input(day: int, file: str) -> str:
    document_path = f"inputs/day{day:0>2}/{file}.txt"
    return str(open(document_path).read())
