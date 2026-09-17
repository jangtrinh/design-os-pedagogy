"""Import or generate a draft, then explicitly apply its two-file manifest."""
import argparse
import json
import re
import sys
from pathlib import Path

from .process import run_provider
from .publication import prepare, apply
from .routing import classify_topic, slugify, find_repo_root
from .validation import build_prompt
from .recovery import inspect_publication, recover_publication
from .transactions import read_text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", nargs="?")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--stage", choices=[f"S{i}" for i in range(8)])
    parser.add_argument("-a", "--archetype", default="auto")
    parser.add_argument("--domain")
    parser.add_argument("--id", help="Canonical ASCII ID; filenames retain the Unicode topic")
    parser.add_argument("--input", type=Path, help="Import provider Markdown without a model call")
    parser.add_argument("--provider", help="Executable reading a prompt on stdin and writing Markdown on stdout")
    parser.add_argument("--provider-arg", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", type=Path, metavar="DRAFT_FOLDER")
    parser.add_argument("--inspect-publication", action="store_true", help="Inspect interrupted publication without changing corpus files")
    parser.add_argument("--recover-publication", action="store_true", help="Explicitly finish an unchanged interrupted publication")
    parser.add_argument("--no-commit", action="store_true", help="Compatibility flag; all runs avoid Git operations")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve() if args.root else find_repo_root()
        if not (root / "README.md").is_file() or not (root / "00-system/metadata-schema.yaml").is_file():
            raise ValueError("Select an existing Agent Teacher checkout")
        if args.inspect_publication or args.recover_publication:
            if (args.inspect_publication and args.recover_publication) or args.topic or args.input or args.provider or args.apply or args.dry_run:
                raise ValueError("Select only --inspect-publication or --recover-publication")
            result = inspect_publication(root) if args.inspect_publication else recover_publication(root)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 2 if result["state"] == "conflict" else 0
        if args.apply:
            if args.topic or args.input or args.provider or args.dry_run:
                raise ValueError("--apply accepts only a previously prepared draft folder")
            folder = args.apply if args.apply.is_absolute() else root / args.apply
            print(json.dumps(apply(root, folder), ensure_ascii=False, indent=2))
            return 0
        if not args.topic or len(args.topic) > 160 or "\n" in args.topic:
            raise ValueError("Provide a single-line topic up to 160 characters")
        route = classify_topic(args.topic, args.archetype, stage=args.stage, domain=args.domain)
        slug = slugify(args.topic)
        identifier = args.id or f"{route['type']}-{slug}"
        if not re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", identifier):
            raise ValueError("Use --id for a canonical ASCII identifier; Unicode filenames are retained")
        prompt = build_prompt(args.topic, route, identifier, (root / "00-system/metadata-schema.yaml").read_text())
        if args.dry_run:
            print(json.dumps({"id": identifier, "route": route, "target": f"{route['dir']}/{slug}.md",
                              "prompt": prompt, "writes": False, "provider_calls": False}, ensure_ascii=False, indent=2))
            return 0
        if bool(args.input) == bool(args.provider):
            raise ValueError("Choose one --input Markdown file or explicit --provider executable")
        if args.input:
            text = read_text(args.input)
        else:
            text = run_provider([args.provider, *args.provider_arg], prompt, timeout=args.timeout)
        draft = prepare(root, route, identifier, slug, text)
        print(json.dumps({"status": "draft", "folder": str(draft.relative_to(root)),
                          "corpus_changed": False, "git_operations": False,
                          "next": "Review module.md, moc.md and manifest.json, then use --apply DRAFT_FOLDER"},
                         ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Publication stopped: {error}", file=sys.stderr)
        return 2
