from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from .diagnostics import ConsoleLogSink, Logger
from .errors import AppError
from .settings import Settings


@dataclass
class CliArguments:
    debug: bool = False


def parse_args(argv: list[str]) -> CliArguments:
    parser = argparse.ArgumentParser(
        prog="geo-organizer",
        usage="geo-organizer [--debug]",
        description="Organizer tool for the geo ecosystem's AI tooling — generates Claude Code skills, agents, and MCP servers.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="override settings.json's debug flag",
    )

    args = parser.parse_args(argv)

    return CliArguments(debug=args.debug)


def main(argv: list[str] | None = None, settings_path: Path | None = None) -> int:
    arguments = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        settings = Settings.load() if settings_path is None else Settings.load(path=settings_path)
    except AppError as error:
        print(f"geo-organizer: error: {error}", file=sys.stderr)
        return 1

    debug = settings.debug or arguments.debug

    Logger.set_logger(
        ConsoleLogSink(
            min_level=settings.logging,
            categories=settings.log_categories,
            excluded_categories=settings.excluded_categories,
        )
    )
    try:
        Logger.info("geo-organizer: started.")
        Logger.info("geo-organizer: completed.")
        return 0
    except AppError as error:
        if debug:
            raise
        print(f"geo-organizer: error: {error}", file=sys.stderr)
        return 1
    finally:
        Logger.set_logger(None)


if __name__ == "__main__":
    raise SystemExit(main())
