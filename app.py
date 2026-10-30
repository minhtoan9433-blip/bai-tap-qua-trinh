"""Lối chạy tương thích; file chính là Khoa học Màu sắc.py."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name('Khoa học Màu sắc.py')), run_name="__main__")
