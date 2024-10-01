import os
from pathlib import Path
from subprocess import run
from pathlib import Path
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--org", "-o", type=str, default="cigna", help="Organization name for the repository (defaults to 'Cigna')")
    parser.add_argument("--file", "-f", type=str, default=None, help="Get URL for file in repository instead of current directory")
    args = parser.parse_args()

    remote_repo = run(
        ["git config --get remote.origin.url"],
        capture_output=True, 
        text=True,
        shell=True
    ).stdout.strip()
    remote_url = remote_repo.rstrip(".git").replace("git@", "https://").replace(f":{args.org}", f"/{args.org}")
    repo_name = remote_url.split("/")[-1]
    branch = run(
        ["git branch --show-current"],
        capture_output=True,
        text=True,
        shell=True
    ).stdout.strip()
    path = Path(os.getcwd())
    git_root_path = None
    while(path.parent != path):
        config_path = path / ".git" / "config"
        if config_path.exists():
            if f"url = {remote_repo}" in open(config_path, "r").read():
                git_root_path = path
                break
        path = path.parent
    if git_root_path:
        rel_path = os.path.relpath(os.getcwd(), git_root_path)
        if args.file:
            new_url = remote_url + "/blob/" + branch + "/" + rel_path + "/" + args.file
        else:
            new_url = remote_url + "/tree/" + branch + "/" + rel_path
        print(new_url)


