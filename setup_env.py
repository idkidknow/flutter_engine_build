import os
import subprocess
from pathlib import Path


def run(*args):
    return subprocess.run(args)


root_dir = Path(os.getcwd())
flutter_dir = root_dir.joinpath("flutter")
os.makedirs(flutter_dir, exist_ok=True)

with open(".gclient.template") as temp:
    gclient = temp.read()
    gclient = gclient.replace("{hash}", os.environ["FLUTTER_HASH"])
    with open(flutter_dir.joinpath(".gclient"), "w") as f:
        f.write(gclient)

if not root_dir.joinpath("depot_tools").exists():
    run(
        "git",
        "clone",
        "https://chromium.googlesource.com/chromium/tools/depot_tools.git",
        "--depth",
        "1",
    )

os.environ["PATH"] += f":{root_dir.joinpath('depot_tools')}"

os.chdir(flutter_dir)
run("gclient", "sync", "--no-history")
