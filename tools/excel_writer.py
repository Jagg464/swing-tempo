"""Write the financial summary workbook (openpyxl) under OUTPUT_ROOT; return its path."""
import os
from config import settings


def write_workbook(extracted_numbers: dict, variance: dict, filename: str) -> str:
    out_dir = settings.OUTPUT_ROOT or "./output"
    path = os.path.join(out_dir, filename)
    if settings.DRY_RUN:
        print(f"[dry-run] would write workbook -> {path}")
        return path
    raise NotImplementedError("Implement openpyxl financial summary workbook.")