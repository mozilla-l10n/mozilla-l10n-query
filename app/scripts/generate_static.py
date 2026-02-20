#!/usr/bin/env python3
"""Generate static JSON files for GitHub Pages deployment."""

import argparse
import json
import os
from pathlib import Path


def read_locale_file(filepath):
    """Read a locale file and return a sorted list of locales."""
    filepath = Path(filepath)
    if not filepath.exists():
        return []
    locales = [
        line.strip() for line in filepath.read_text().splitlines() if line.strip()
    ]
    return sorted(locales)


def load_json(filepath):
    """Load and return a JSON file."""
    return json.loads(Path(filepath).read_text())


def generate_all_repos(source_path):
    """Return data for all repositories (index endpoint)."""
    source_path = Path(source_path)
    repos_data = load_json(source_path / "repositories.json")
    result = []
    for repo in repos_data.values():
        result.append(
            {
                "id": repo["id"],
                "display_order": repo["display_order"],
                "name": repo["name"],
                "locales": read_locale_file(source_path / repo["locales"]),
                "type": repo["type"],
                "enabled": repo["enabled"],
            }
        )
    return result


def generate_single_repo(source_path, repo_id):
    """Return data for a single repository, or None if unknown."""
    source_path = Path(source_path)
    repos_data = load_json(source_path / "repositories.json")
    if repo_id not in repos_data:
        return None
    repo = repos_data[repo_id]
    return {
        "id": repo["id"],
        "name": repo["name"],
        "display_order": repo["display_order"],
        "locales": read_locale_file(source_path / repo["locales"]),
        "type": repo["type"],
        "enabled": repo["enabled"],
    }


def generate_type_repos(source_path, repo_type):
    """Return data for repositories of a specific type."""
    source_path = Path(source_path)
    repos_data = load_json(source_path / "repositories.json")
    result = []
    for repo in repos_data.values():
        if repo["type"] == repo_type:
            result.append(
                {
                    "id": repo["id"],
                    "display_order": repo["display_order"],
                    "name": repo["name"],
                    "locales": read_locale_file(source_path / repo["locales"]),
                    "type": repo["type"],
                    "enabled": repo["enabled"],
                }
            )
    return result


def generate_bugzilla(source_path, product):
    """Return Bugzilla component data for www or product."""
    source_path = Path(source_path)
    bugzilla_data = load_json(source_path / "bugzilla_components.json")
    locale_list = "cf_locale" if product == "www" else "mozilla_localizations"
    return {
        locale: data["full_name"] for locale, data in bugzilla_data[locale_list].items()
    }


def generate_tool(source_path, tool):
    """Return locale data for a specific tool or all tools."""
    source_path = Path(source_path)
    supported_tools = ["pontoon", "pontoon-mozorg"]
    if tool == "all":
        return {
            t: read_locale_file(source_path / "tools" / f"{t}.txt")
            for t in supported_tools
        }
    if tool in supported_tools:
        return read_locale_file(source_path / "tools" / f"{tool}.txt")
    return []


def write_json(output_path, data):
    """Write JSON to a file, creating parent directories as needed."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"  Written: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate static JSON files for GitHub Pages."
    )
    parser.add_argument("--source", default="app/sources/", help="Path to source files")
    parser.add_argument(
        "--output", default="docs/api/", help="Path to output directory"
    )
    args = parser.parse_args()

    root = Path(__file__).parent.parent.parent

    if os.environ.get("AUTOMATED_TESTS"):
        source_path = root / "tests" / "testfiles"
    else:
        source_path = Path(args.source)
        if not source_path.is_absolute():
            source_path = root / args.source

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = root / args.output

    print(f"Source: {source_path}")
    print(f"Output: {output_path}")

    repos_data = load_json(source_path / "repositories.json")

    print("\nGenerating index.json...")
    write_json(output_path / "index.json", generate_all_repos(source_path))

    print("\nGenerating repo/*.json...")
    for repo_id in repos_data:
        write_json(
            output_path / "repo" / f"{repo_id}.json",
            generate_single_repo(source_path, repo_id),
        )

    print("\nGenerating type/*.json...")
    for repo_type in ["product", "web"]:
        write_json(
            output_path / "type" / f"{repo_type}.json",
            generate_type_repos(source_path, repo_type),
        )

    print("\nGenerating bugzilla/*.json...")
    for product in ["www", "product"]:
        write_json(
            output_path / "bugzilla" / f"{product}.json",
            generate_bugzilla(source_path, product),
        )

    print("\nGenerating tool/*.json...")
    for tool in ["pontoon", "pontoon-mozorg", "all"]:
        write_json(
            output_path / "tool" / f"{tool}.json", generate_tool(source_path, tool)
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
