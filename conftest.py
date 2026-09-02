"""Cấu hình pytest cho toàn bộ kho."""
import sys
from pathlib import Path

# Thêm gốc kho vào sys.path để import tools
sys.path.insert(0, str(Path(__file__).parent))
