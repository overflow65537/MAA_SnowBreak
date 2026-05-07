#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def deep_merge(base, overlay):
    if isinstance(base, dict) and isinstance(overlay, dict):
        merged = dict(base)
        for key, value in overlay.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    return overlay


def dump_json(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)
        file.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Merge an upstream interface schema with a custom overlay."
    )
    parser.add_argument("--base", required=True, help="Path to the upstream schema")
    parser.add_argument(
        "--custom", required=True, help="Path to the custom schema overlay"
    )
    parser.add_argument(
        "--output", required=True, help="Path to write the merged schema"
    )
    args = parser.parse_args()

    merged = deep_merge(load_json(args.base), load_json(args.custom))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dump_json(output_path, merged)


if __name__ == "__main__":
    main()