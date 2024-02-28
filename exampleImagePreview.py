# pip install marimo
# then navigate to the directory containing this file and run "marimo run exampleImagePreview.py"
# or run from VSCode with the Marimo extension installed 
# (there's a little orange lightning bolt in the top right of the window)

import marimo

__generated_with = "0.2.9"
app = marimo.App()


@app.cell
def __():
    import astropy.io.fits as fits
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import glob
    import astropy.visualization as vis
    import marimo as mo

    plt.style.use("dark_background")
    return fits, glob, mo, np, os, plt, vis


@app.cell
def __(mo, os):
    # Get list of subdirectories in data directory that don't start with _
    dir_list = [
        d for d in os.listdir() if os.path.isdir(d) and not (d.startswith("_") or d.startswith("."))
    ]

    chosen_dir = dir_list[0]

    # Make dropdown menu for directories
    dir_dropdown = mo.ui.dropdown(
        dir_list, value=chosen_dir, label="Choose a directory: "
    )

    # dir_hstack = mo.md(f"Choose a directory: {dir_dropdown}")

    vmin = mo.ui.slider(
        0, 2000, step=50, label="Min value: ", debounce=True, value=0
    )
    vmax = mo.ui.slider(
        1000, 2000, step=50, label="Max value: ", debounce=True, value=1500
    )

    pmin = mo.ui.number(
        0, 100, step=1, label="Min percent: ", debounce=True, value=15
    )

    pmax = mo.ui.number(
        0, 100, step=1, label="Min percent: ", debounce=True, value=99.7
    )

    normalization = mo.ui.dropdown(
        ["linear", "log", "sqrt"], value="linear", label="Normalization: "
    )

    stretch_mode = mo.ui.dropdown(["MinMax", "Percentile"], value="MinMax", label="Stretch Mode")
    return (
        chosen_dir,
        dir_dropdown,
        dir_list,
        normalization,
        pmax,
        pmin,
        stretch_mode,
        vmax,
        vmin,
    )


@app.cell
def __(dir_dropdown, glob, mo, os):
    # Get list of images in chosen directory (only show filenames, not full paths)
    image_list = [
        os.path.basename(f)
        for f in glob.glob(os.path.join(dir_dropdown.value, "*.f*ts"))
    ]


    # Make dropdown menu for images
    image_dropdown = mo.ui.dropdown(
        image_list,
        value=image_list[0] if len(image_list) > 0 else None,
        label="Choose an image: ",
    )  # Get list of images in chosen directory

    # image_selector = mo.md(f"Choose an image: {image_dropdown}")
    return image_dropdown, image_list


@app.cell
def __(dir_dropdown, fits, image_dropdown):
    file = None
    if image_dropdown.value is not None:
        file = dir_dropdown.value + "/" + image_dropdown.value
        image = fits.getdata(file)
        if len(image.shape) == 3:
            image = image[0]
    return file, image


@app.cell
def __(
    dir_dropdown,
    image_dropdown,
    mo,
    pmax,
    pmin,
    stretch_mode,
    vmax,
    vmin,
):
    mo.vstack([mo.md("Note, the cutout images (from legacysurvey.com) do not have the same pixel value range (they seem to be floats instead of ints), so min/max sliders won't work for these. Feel free to fix this and I'll be happy to merge a pull request."), dir_dropdown, image_dropdown,mo.hstack([vmin, mo.md(f"Min: {vmin.value}"), vmax,mo.md(f"Max: {vmax.value}")]),mo.hstack([pmin, pmax]), stretch_mode])
    return


@app.cell
def __(image, image_dropdown, plt, stretch_mode, vmax, vmin):
    # Generate plot
    #_image = fits.getdata(file)
    #norm = vis.simple_norm(image, stretch=normalization.value, min_cut=vmin.value, max_cut=vmax.value)
    if stretch_mode.value == "MinMax":
        plt.imshow(
            image, cmap="cividis", vmin=vmin.value, vmax=vmax.value
        )
        plt.title(image_dropdown.value)
        plt.colorbar()
        # tight layout
        plt.tight_layout()

    plt.gca() if stretch_mode.value == "MinMax" else None
    return


@app.cell
def __(image, image_dropdown, plt, pmax, pmin, stretch_mode, vis):
    if stretch_mode.value == "Percentile":
        _interval = vis.AsymmetricPercentileInterval(pmin.value, pmax.value)
        _vmin, _vmax = _interval.get_limits(image)
        plt.imshow(image, cmap="cividis", vmin=_vmin, vmax=_vmax)
        plt.title(image_dropdown.value)
        plt.colorbar()
        # tight layout
        plt.tight_layout()
    plt.gca() if stretch_mode.value == "Percentile" else None
    return


if __name__ == "__main__":
    app.run()
