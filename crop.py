import os
import argparse
from pathlib import Path
import cv2
import numpy as np

from PIL import Image


def get_file_list(dir, extensions):
    _files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

    files = list()
    for file in _files:
        if file.split(".")[-1].lower() in extensions:
            files.append(file)

    return files


def main(base_dir, files, extention):

    for file in files:
        print("Processing %s..." % (str(file)))
        img = cv2.imread(base_dir / file, cv2.IMREAD_UNCHANGED)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

        coords = cv2.findNonZero(thresh)

        x, y, w, h = cv2.boundingRect(coords)

        cropped = img[y : y + h, x : x + w]

        fname = file.split(".")
        fname.pop(len(fname) - 1)
        fname = ".".join(fname)

        cv2.imwrite(base_dir / "cropped" / f"{fname}.{extention}", cropped)

        """
        if remove_alpha:
            png = img_resize.convert("RGBA")
            background = Image.new("RGBA", png.size, (255, 255, 255))

            img_resize = Image.alpha_composite(background, png)

        if convert is not None:
            img_resize = img_resize.convert(convert)
        """


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dir", type=str, default=None)
    parser.add_argument(
        "--width",
        type=int,
        default=180,
        help="180 for double column, 90 for single column.",
    )
    parser.add_argument("--dpi", type=int, default=500)

    args = parser.parse_args()

    # width in mm
    width = args.width

    # dpi
    dpi = args.dpi

    # extensions
    exts = ["png", "jpeg", "jpg"]

    # save params
    # convert : RGB, RGBA, None
    # remove_alpha = True
    # convert = "RGB"
    extention = "png"
    # quality = 95

    if args.dir is None:
        import tkinter, tkinter.filedialog

        base_dir = tkinter.filedialog.askdirectory(
            initialdir=Path.home(), mustexist=True
        )
        base_dir = Path(base_dir)
    else:
        base_dir = Path(args.dir)
    print("target directory: %s" % (str(base_dir)))

    (base_dir / "cropped").mkdir(parents=True, exist_ok=True)

    files = get_file_list(base_dir, exts)
    if len(files) == 0:
        raise RuntimeError("No files are found.")
    print("The following files were found.")
    for file in files:
        print(file)

    main(
        base_dir=base_dir,
        files=files,
        extention=extention,
    )
