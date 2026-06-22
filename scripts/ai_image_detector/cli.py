from __future__ import annotations

import argparse
import json
from pathlib import Path

from .inspector import analyze_file, write_reports


def main() -> int:
    parser = argparse.ArgumentParser(description="检测图片是否存在 AI 生成/AI 合成证据，并生成中文报告。")
    parser.add_argument("images", nargs="+", help="要检测的图片路径。")
    parser.add_argument("--ocr", action="store_true", help="运行 tesseract OCR，检查画面里的可见水印文字。")
    parser.add_argument("--output-dir", help="Write JSON and HTML reports to this directory.")
    parser.add_argument("--artifacts-dir", help="Write auxiliary forensic artifacts, such as FFT spectrum images.")
    parser.add_argument(
        "--content-assessment",
        choices=["likely_ai", "possible_ai", "unclear", "likely_not_ai", "not_provided"],
        default="not_provided",
        help="把视觉/内容层面的 AI 疑似判断写入报告。",
    )
    parser.add_argument(
        "--content-note",
        action="append",
        default=[],
        help="添加视觉/内容疑似理由，可重复传入。",
    )
    args = parser.parse_args()

    results = []
    for image in args.images:
        content_assessment = {
            "label": args.content_assessment,
            "notes": args.content_note,
        }
        result = analyze_file(
            image,
            enable_ocr=args.ocr,
            artifacts_dir=args.artifacts_dir,
            content_assessment=content_assessment,
        )
        if args.output_dir:
            result["reports"] = write_reports(result, Path(args.output_dir))
        results.append(result)

    payload = results[0] if len(results) == 1 else {"results": results}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
