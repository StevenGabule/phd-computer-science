"""CLI entry point for downloading the CAP bulk dump.

Run::

    python scripts/download_cap.py --jurisdictions us
    python scripts/download_cap.py --jurisdictions us,ny --dest /mnt/data/cap
    python scripts/download_cap.py --dry-run

Defaults pull only the U.S. Supreme Court jurisdiction (~small) so a first run
finishes in minutes rather than days.
"""
from __future__ import annotations

import logging
from pathlib import Path

import click

from citecheck.config import PATHS, ensure_dirs
from citecheck.data.cap_loader import (
    CAP_DEFAULT_JURISDICTIONS,
    CAP_EXPORTS_BASE,
    download_cap_bulk,
)

logger = logging.getLogger(__name__)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--dest",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help=f"Destination directory. Defaults to {PATHS.cap_raw}.",
)
@click.option(
    "--jurisdictions",
    type=str,
    default=",".join(CAP_DEFAULT_JURISDICTIONS),
    help=(
        "Comma-separated CAP jurisdiction slugs (e.g. 'us,ny,cal'). "
        "Pass 'all' to download every jurisdiction (~100 GB, multi-day)."
    ),
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Show the URLs that would be downloaded without fetching anything.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable DEBUG-level logging.",
)
def main(dest: Path | None, jurisdictions: str, dry_run: bool, verbose: bool) -> None:
    """Download CAP bulk per-jurisdiction archives to ``--dest``."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    ensure_dirs()
    target_dir = dest if dest is not None else PATHS.cap_raw

    if jurisdictions.strip().lower() == "all":
        jur_list: list[str] | None = None
    else:
        jur_list = [j.strip() for j in jurisdictions.split(",") if j.strip()]
        if not jur_list:
            raise click.UsageError("--jurisdictions must be 'all' or a non-empty list.")

    if dry_run:
        items = jur_list or ["<full corpus -- requires scrape of exports index>"]
        click.echo(f"Would download to: {target_dir}")
        for jur in items:
            click.echo(f"  {CAP_EXPORTS_BASE}/{jur}_text.tar.gz")
        return

    click.echo(
        f"Downloading {len(jur_list) if jur_list else 'ALL'} jurisdiction(s) to {target_dir}"
    )
    download_cap_bulk(dest=target_dir, only_jurisdictions=jur_list)
    click.echo("Done.")


if __name__ == "__main__":
    main()
