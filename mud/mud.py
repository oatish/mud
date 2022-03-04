from argparse import ArgumentParser
import os
from parse import infer_modules_info
from document import document_all_md


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        default="",
        help="Short description of package.",
    )
    parser.add_argument(
        "-r",
        "--readme",
        action="store_true",
        help="Include README.md as package description.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="MODULES.md",
        help="Output file to save documentation.",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=os.path.basename(os.getcwd()).upper(),
        help="Name of package.",
    )
    parser.add_argument(
        "-p",
        "--paths",
        type=str,
        default="./",
        help="Root directory to search for modules.",
    )
    args = parser.parse_args()

    description_section = args.description
    if args.readme:
        with open("README.md", "r") as f:
            description_section = f.read()
    inferred_modules = infer_modules_info(args.paths)
    documentation = document_all_md(
        inferred_modules, args.name, description=description_section
    )
    print(documentation)
    with open(args.output, "w") as f:
        f.write(documentation.strip())


if __name__ == "__main__":
    main()
