"""Write the FinCom memo to a Word document (Georgia font, US Letter, 1in margins).
Live: build with python-docx (or the docx skill approach) and save under OUTPUT_ROOT."""
import os
from config import settings


def write_memo(memo_text: str, filename: str) -> str:
    out_dir = settings.OUTPUT_ROOT or "./output"
    path = os.path.join(out_dir, filename)
    if settings.DRY_RUN:
        print(f"[dry-run] would write FinCom memo -> {path}")
        return path
    raise NotImplementedError("Implement python-docx memo writer (Georgia, US Letter, 1in).")