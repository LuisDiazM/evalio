ALLOWED_FORMATS = ["text/csv"]
MAX_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_COLUMNS = ["Documento", "Nombre"]


def validate_file(content_type: str, size: int) -> bool:
    return content_type in ALLOWED_FORMATS and size <= MAX_SIZE


def validate_columns_csv(columns: list[str]) -> bool:
    return all(elem in columns for elem in ALLOWED_COLUMNS)
