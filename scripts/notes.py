import os
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime as dt


EDITOR = "nvim"
AUTHOR_NAME = "shane stephenson"
AUTHOR_EMAIL = "shane.stephenson@evernorth.com"
TEMPLATE_MD = """--------------------
### {}

> subject: {} \\
> author: {} ({}) \\
> date: {} \\

--------------------


"""

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--extension",
        "-e",
        type=str,
        default="md",
        help="the extension format of the file",
    )
    parser.add_argument(
        "--name", "-n", type=str, help="optional name suffix for notes file"
    )
    parser.add_argument("--title", "-t", type=str, help="optional title for notes file")
    parser.add_argument(
        "--subject", "-s", type=str, default="", help="description for notes"
    )
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        default="notes/notes",
        help="optional file path of notes folder",
    )
    parser.add_argument(
        "--author", "-a", type=str, default=AUTHOR_NAME, help="author name"
    )
    parser.add_argument(
        "--email", "-E", type=str, default=AUTHOR_EMAIL, help="author email"
    )
    parser.add_argument(
        "--sections",
        "-S",
        nargs="+",
        default=["context", "notes", "todo"],
        type=str,
        help="section titles for notes",
    )
    parser.add_argument(
        "--uppercase",
        "-u",
        action="store_true",
        help="flag to convert section titles to uppercase",
    )
    parser.add_argument(
        "--lowercase",
        "-l",
        action="store_true",
        help="flag to convert section titles to lowercase",
    )
    parser.add_argument(
        "--removedate",
        "-r",
        action="store_true",
        help="flag to remove appending date to notes file",
    )
    args = parser.parse_args()
    n = args.name
    now = dt.now()
    if not n:
        n_suffix = now.strftime("%Y%m%d-%H%M%S")
        n = f"notes-{n_suffix}"
    else:
        if not args.removedate:
            n_suffix = now.strftime("%Y%m%d")
            n = f"{n}-{n_suffix}"
    if not args.title:
        args.title = f"notes for {now.strftime('%Y-%m-%d')}"
    casing = (
        lambda s: s.upper() if args.uppercase else s.lower() if args.lowercase else s
    )
    args.sections = [casing(s) for s in args.sections]
    for var in [args.title, TEMPLATE_MD, args.subject, args.author, args.email]:
        var = casing(var)
    filename = Path.home() / args.path / f"{n}.{args.extension}"
    print(f"Creating file: {filename}")
    with open(filename, "w") as f:
        f.write(
            TEMPLATE_MD.format(
                args.title,
                args.subject,
                args.author,
                args.email,
                now.strftime("%Y-%m-%d"),
            )
        )
        for section in args.sections:
            f.write(f"#### <ins>{section}</ins>\n\n")
    print(f"Opening file with {EDITOR}")
    os.system(f"{EDITOR} {filename}")
