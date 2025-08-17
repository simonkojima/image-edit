import os
import argparse

from PIL import Image


def get_file_list(dir, extensions):
    _files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

    files = list()
    for file in _files:
        if file.split(".")[-1].lower() in extensions:
            files.append(file)

    return files


def main(base_dir, files, width, dpi, remove_alpha, convert, extention, quality):

    for file in files:
        print("Processing %s..." % (str(file)))
        img = Image.open(os.path.join(base_dir, file))
        w, h = img.size

        w_new = width / 22.54 * dpi

        h_new = h * w_new / w

        size_new = (int(w_new), int(h_new))

        img_resize = img.resize(size_new)

        if remove_alpha:
            png = img_resize.convert("RGBA")
            background = Image.new("RGBA", png.size, (255, 255, 255))

            img_resize = Image.alpha_composite(background, png)

        if convert is not None:
            img_resize = img_resize.convert(convert)

        fname = file.split(".")
        fname.pop(len(fname) - 1)
        fname = ".".join(fname)

        img_resize.save(
            os.path.join(base_dir, "resized", "%s.%s" % (fname, extention)),
            quality=quality,
        )


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
    remove_alpha = True
    convert = "RGB"
    extention = "jpg"
    quality = 95

    if args.dir is None:
        import tkinter, tkinter.filedialog

        base_dir = tkinter.filedialog.askdirectory(
            initialdir=os.path.expanduser("~"), mustexist=True
        )
    else:
        base_dir = args.dir
    print("target directory: %s" % (str(base_dir)))

    def mkdir(dir):
        isExist = os.path.exists(dir)
        if not isExist:
            os.makedirs(dir)

    mkdir(os.path.join(base_dir, "resized"))

    files = get_file_list(base_dir, exts)
    if len(files) == 0:
        raise RuntimeError("No files are found.")
    print("The following files were found.")
    for file in files:
        print(file)

    main(
        base_dir=base_dir,
        files=files,
        width=width,
        dpi=dpi,
        remove_alpha=remove_alpha,
        convert=convert,
        extention=extention,
        quality=quality,
    )
