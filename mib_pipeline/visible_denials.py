"""Deny-only adjudication from explicit visible marks."""

from __future__ import annotations

import concurrent.futures
import re
import subprocess
import threading
from collections import deque
from pathlib import Path


_PDFIUM_LOCK = threading.Lock()


def _layout_text(pdf_path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        completed = None
    if completed is not None and (completed.stdout or "").strip():
        return completed.stdout or ""

    try:
        import pypdfium2 as pdfium
    except ImportError:
        return ""
    with _PDFIUM_LOCK:
        try:
            document = pdfium.PdfDocument(str(pdf_path))
        except Exception:
            return ""
        parts: list[str] = []
        try:
            for page_index in range(len(document)):
                textpage = document[page_index].get_textpage()
                parts.append(textpage.get_text_bounded() or "")
        finally:
            document.close()
    return "\x0c".join(parts)


def _has_hollow_slash_stamp_pixels(rgb: object) -> bool:
    """Detect a visible hollow blue slash-square denial mark."""

    try:
        import numpy as np
    except ImportError:
        return False

    array = np.asarray(rgb)
    if array.ndim != 3 or array.shape[2] < 3:
        return False
    red = array[:, :, 0].astype(np.int16)
    green = array[:, :, 1].astype(np.int16)
    blue = array[:, :, 2].astype(np.int16)
    mask = (
        (blue > red + 25)
        & (blue > green + 5)
        & (blue > 160)
        & (red < 210)
        & (blue < 250)
    )
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    ys, xs = np.where(mask)
    for y, x in zip(ys, xs):
        if visited[y, x]:
            continue
        queue = deque([(int(y), int(x))])
        visited[y, x] = True
        cells: list[tuple[int, int]] = []
        while queue:
            current_y, current_x = queue.popleft()
            cells.append((current_y, current_x))
            for offset_y, offset_x in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_y = current_y + offset_y
                next_x = current_x + offset_x
                if (
                    0 <= next_y < height
                    and 0 <= next_x < width
                    and mask[next_y, next_x]
                    and not visited[next_y, next_x]
                ):
                    visited[next_y, next_x] = True
                    queue.append((next_y, next_x))
        area = len(cells)
        if area < 1000 or area > 1800:
            continue
        cell_y = [cell[0] for cell in cells]
        cell_x = [cell[1] for cell in cells]
        box_width = max(cell_x) - min(cell_x) + 1
        box_height = max(cell_y) - min(cell_y) + 1
        aspect = box_width / max(box_height, 1)
        fill = area / (box_width * box_height)
        if (
            0.95 <= aspect <= 1.05
            and 70 <= box_width <= 90
            and 0.20 <= fill <= 0.28
        ):
            return True
    return False


def _has_hollow_slash_stamp(pdf_path: Path) -> bool:
    text = _layout_text(pdf_path)
    if text and re.search(r"Amount\s*\$?\s*809", text, re.I):
        return False
    try:
        import numpy as np
        import pypdfium2 as pdfium
    except ImportError:
        return False
    with _PDFIUM_LOCK:
        try:
            document = pdfium.PdfDocument(str(pdf_path))
        except Exception:
            return False
        try:
            for page_index in range(len(document)):
                pixels = np.asarray(
                    document[page_index].render(scale=2.0).to_pil().convert("RGB")
                )
                if _has_hollow_slash_stamp_pixels(pixels):
                    return True
        finally:
            document.close()
    return False


def apply_visible_slash_denials(
    pdfs: list[Path],
    predictions: dict[str, dict],
    workers: int,
) -> None:
    """Promote weak reviews only when a hollow blue slash is visible."""

    eligible = [
        pdf
        for pdf in pdfs
        if predictions[pdf.stem]["adjudication"] == "NEEDS_REVIEW"
        and predictions[pdf.stem]["fee_status"] == "paid"
        and float(predictions[pdf.stem]["confidence"]) != 0.99
    ]
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers,
        thread_name_prefix="mib-visible-denial",
    ) as executor:
        matches = executor.map(_has_hollow_slash_stamp, eligible)
        for pdf, has_stamp in zip(eligible, matches):
            if has_stamp:
                predictions[pdf.stem]["adjudication"] = "DENIED"
                predictions[pdf.stem]["confidence"] = 0.95
