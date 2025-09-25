import os
import subprocess
from pathlib import Path
import shutil


def run(*args):
    return subprocess.run(args)


root_dir = Path(os.getcwd())

os.environ["PATH"] += f":{root_dir.joinpath('depot_tools')}"

output_dir = root_dir.joinpath("output")
os.makedirs(output_dir, exist_ok=True)

engine_src_dir = root_dir.joinpath("engine/src")
os.chdir(engine_src_dir)

match os.environ["RUNTIME_MODE"]:
    case "DEBUG":
        run(
            "flutter/tools/gn",
            "--runtime-mode",
            "debug",
            "--unoptimized",
            "--enable-fontconfig",
            "--enable-vulkan",
            "--disable-desktop-embeddings",
            "--no-build-embedder-examples",
        )
        run("ninja", "-C", "out/host_debug_unopt")
        shutil.copyfile(
            engine_src_dir.joinpath("out/host_debug_unopt/libflutter_engine.so"),
            output_dir.joinpath("libflutter_engine.so.DEBUG"),
        )
    case "PROFILE":
        run(
            "flutter/tools/gn",
            "--runtime-mode",
            "profile",
            "--no-lto",
            "--enable-fontconfig",
            "--enable-vulkan",
            "--disable-desktop-embeddings",
            "--no-build-embedder-examples",
        )
        run("ninja", "-C", "out/host_profile")
        shutil.copyfile(
            engine_src_dir.joinpath("out/host_profile/libflutter_engine.so"),
            output_dir.joinpath("libflutter_engine.so.PROFILE"),
        )
    case "RELEASE":
        run(
            "flutter/tools/gn",
            "--runtime-mode",
            "release",
            "--enable-fontconfig",
            "--enable-vulkan",
            "--disable-desktop-embeddings",
            "--no-build-embedder-examples",
        )
        run("ninja", "-C", "out/host_release")
        shutil.copyfile(
            engine_src_dir.joinpath("out/host_release/libflutter_engine.so"),
            output_dir.joinpath("libflutter_engine.so.RELEASE"),
        )
