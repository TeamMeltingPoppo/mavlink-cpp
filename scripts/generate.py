from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pymavlink.generator import mavgen
import pymavlink



def load_project(root: Path) -> dict[str, object]:
    with (root / "pyproject.toml").open("rb") as file:
        pyproject = tomllib.load(file)

    try:
        return pyproject["project"]
    except KeyError as error:
        raise RuntimeError(
            "[project] section not found in pyproject.toml"
        ) from error

def clean_generated_dir(output_dir : Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

def generate_mavlink(dialect: Path, mavlink_output_dir: Path) -> None:
    if mavlink_output_dir.exists():
        shutil.rmtree(mavlink_output_dir)

    mavlink_output_dir.mkdir(parents=True)

    options = mavgen.Opts(mavlink_output_dir,"2.0","C++11")

    if not mavgen.mavgen(options, [dialect]):
        raise RuntimeError("MAVLink code generation failed")

def create_package(context: dict[str, object], template_dir: Path, mavlink_output_dir: Path , output_dir: Path, archive_filename: str) -> None:

    generated_dir = output_dir / "generated"

    environment = Environment(
        loader=FileSystemLoader(template_dir),
        keep_trailing_newline=True,
    )

    if not generated_dir.exists():
        generated_dir.mkdir(parents=True)

    for source in template_dir.rglob("*"):
        if not source.is_file():
            continue

        print(f"Generating: {source.relative_to(template_dir)}")
        relative_path = source.relative_to(template_dir)
        template = environment.get_template(relative_path.as_posix())

        destination = generated_dir / relative_path.with_suffix("")
        destination.parent.mkdir(parents=True, exist_ok=True)

        destination.write_text(
            template.render(**context),
            encoding="utf-8",
        )

    shutil.copytree(
        mavlink_output_dir,
        generated_dir / "include" / "mavlink",
    )
    archive_path = output_dir / f"{archive_filename}.zip"
    shutil.make_archive(
        base_name=archive_path.with_suffix(""),
        format="zip",
        root_dir=generated_dir,
    )


def main() -> None:
  
    ROOT = Path(__file__).resolve().parent.parent
    ARCHIVE_FILENAME = "mavlink-cpp"

    TEMPLATE_DIR = ROOT / "templates"
    OUTPUT_DIR = ROOT / "dist"
    MAVLINK_OUTPUT_DIR = OUTPUT_DIR / "mavlink"

    project = load_project(ROOT)
    dialect = ROOT / "mavlink-dialect" / "dialects" / "swingby.xml"

    context = {
        "project": project,
        "pymavlink_version": pymavlink.__version__,
    }

    print(f"Project:  {project['name']} {project['version']}")
    print(f"Dialect:  {dialect}")
    print(f"Templates: {TEMPLATE_DIR}")

    clean_generated_dir(OUTPUT_DIR)
    generate_mavlink(dialect, MAVLINK_OUTPUT_DIR)
    create_package(context, TEMPLATE_DIR, MAVLINK_OUTPUT_DIR, OUTPUT_DIR, ARCHIVE_FILENAME)


if __name__ == "__main__":
    main()