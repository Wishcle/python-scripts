import argparse
import shutil
from pathlib import Path

from tqdm import tqdm


def main() -> None:
    src_root = get_path_from_args()
    src_paths = list(src_root.rglob("*"))

    path_out = Path("data/canon")
    shutil.rmtree(path_out, ignore_errors=True)
    path_out.mkdir(parents=True)

    for src_path in tqdm(src_paths):
        new_path = path_out / src_path.relative_to(src_root)
        new_path = Path(str(new_path).replace("_MG", "IMG"))

        if src_path.is_dir():
            new_path.mkdir()
        else:
            assert new_path.parent.exists(), f"'{new_path.parent}' does not exist yet?!"
            shutil.copyfile(src_path, new_path)


def get_path_from_args() -> Path:
    parser = argparse.ArgumentParser(description="Process an image directory.")
    parser.add_argument(
        "-d", "--imgdir", type=str, required=True,
        help="Path to the folder of images to rename.")
    args = parser.parse_args()

    path = Path(args.imgdir)
    assert path.exists()
    return path
