import datetime
import json
from os import path
from os.path import join
from typing import Any, Dict, List
from pathlib import Path
import subprocess


import lmfit as lm
import matplotlib as mpl
import xarray as xr
import os
from quantify_core.data.handling import (
    load_dataset_from_path,
)

REPO_PATH = path.abspath("") #.split("nuclear_spin_snv")[0] + "nuclear_spin_snv"
DATA_PATH = path.join(REPO_PATH, "data")
FIGURE_PATH = path.join(REPO_PATH, "figures")
SUBFIGURE_PATH = path.join(REPO_PATH, "subfigures")
FIGURE_PATH_BASE = "figures/results/"
PATH_TO_OVERLEAF = "C:/Users/timod/Dropbox/Apps/Overleaf/Msc Thesis/"

HZ_TO_KHZ = 1e-3
MHZ_TO_KHZ = 1e3
W_TO_NW = 1e9
GHZ_TO_MHZ = 1e3
KHZ_TO_HZ = 1e3
HZ_TO_GHZ = 1e-9
GHZ_TO_HZ = 1e9
S_TO_US = 1e6
S_TO_NS = 1e9

def _generate_date_time():
    time_stamp = datetime.datetime.now()
    # time_stamp gives microseconds by default
    (date_time, micro) = time_stamp.strftime("%Y%m%d-%H%M%S-.%f").split(".")
    # this ensures the string is formatted correctly as some systems return 0 for micro
    date_time = f"{date_time}{int(int(micro) / 1000):03d}-"
    return date_time


def save_dataset(dataset, folder, name):
    date_time = _generate_date_time()
    file_path = join(folder, date_time + name + ".hdf5")
    # Invalid_netcdf is used to be able to save None and bools as attrs
    dataset.to_netcdf(file_path, engine="h5netcdf", invalid_netcdf=True)


def load_dataset(folder, name):
    return xr.load_dataset(join(folder, name), engine="h5netcdf")


def load_dataset_from_data(
    folder_name: str, dataset_name: str = "dataset_processed"
) -> xr.Dataset:
    return load_dataset(path.join(DATA_PATH, folder_name), f"{dataset_name}.hdf5")


def load_quantities_of_interest_from_data(
    folder_name: str, qoi_name: str = "quantities_of_interest"
) -> Dict:
    # Load JSON file and return
    qoi_path = path.join(DATA_PATH, folder_name, f"{qoi_name}.json")
    with open(path.join(qoi_path), "r") as file:
        quantities_of_interest = json.load(file)
    return quantities_of_interest


# def save_figure(
#     fig, figure_number: int, subfigure_name: str
# ) -> None:
#     fig.savefig(
#         path.join(SUBFIGURE_PATH, f"figure{figure_number}", f"{subfigure_name}.svg"),
#         transparent=True,
#     )
def save_figure(
    fig, figure_number: int, subfigure_name: str, **kwargs
) -> None:

    kwargs.setdefault("transparent", True)
    file_path = path.join(SUBFIGURE_PATH, f"figure{figure_number}", f"{subfigure_name}.svg")
    _ensure_folders_exists(file_path)
    fig.savefig(file_path, dpi=1000, **kwargs)

def _ensure_folders_exists(path_name):
    path = Path(path_name)
    directory = path.parent
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


def save_model_results(results: Dict[str, Any]) -> None:
    for name, r in results.items():
        lm.model.save_modelresult(r, name)


def load_model_results(file_names: List[str], keys: List[str]) -> List[Any]:
    fit_results = {}
    for f, k in zip(file_names, keys):
        fit_results[k] = lm.model.load_modelresult(f)
    return fit_results

def get_files_with_extension(folder_path: str, extension: str) -> list[str]:
    return [folder_path+"/"+f for f in os.listdir(folder_path) if f.endswith(f".{extension}")]

def update_combined_figure(figure_number: int):
    # Run the script to update the combined figure
    svg_path = FIGURE_PATH_BASE + f"figure{figure_number}/figure{figure_number}.svg"
    pdf_path_repo = FIGURE_PATH_BASE + f"figure{figure_number}/figure{figure_number}.pdf"
    pdf_path_dropbox = PATH_TO_OVERLEAF + f"Figures/figure{figure_number}.pdf"
    png_path_repo = FIGURE_PATH_BASE + f"figure{figure_number}/figure{figure_number}.png"
    a = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_repo}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
    b = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_dropbox}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
    c = subprocess.run(["inkscape", svg_path, f"--export-filename={png_path_repo}", f"--export-type=png", "--export-dpi=500"], capture_output=True, text=True, check=True)

def update_all_combined_figures():
    # Run the script to update the combined figure
    for figure_num in os.listdir("figures/results"):
        svg_path = f"figures/results/{figure_num}/{figure_num}.svg"
        pdf_path_repo = f"figures/results/{figure_num}/{figure_num}.pdf"
        png_path_repo = f"figures/results/{figure_num}/{figure_num}.png"
        pdf_path_dropbox = f"C:/Users/timod/Dropbox/Apps/Overleaf/Msc Thesis/Figures/{figure_num}.pdf"
        a = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_repo}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        b = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_dropbox}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        c = subprocess.run(["inkscape", svg_path, f"--export-filename={png_path_repo}", f"--export-type=png", "--export-dpi=500"], capture_output=True, text=True, check=True)



def update_all_theory_figures():
    all_svg_paths = get_files_with_extension("figures/theory", "svg")
    for svg_path in all_svg_paths:
        pdf_path_repo = svg_path.replace("svg", "pdf")
        png_path_repo = svg_path.replace("svg", "png")
        pdf_path_dropbox = f"C:/Users/timod/Dropbox/Apps/Overleaf/MSc Thesis/Figures/" + svg_path.split("/")[-1].replace("svg", "pdf")
        a = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_repo}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        b = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_dropbox}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        c = subprocess.run(["inkscape", svg_path, f"--export-filename={png_path_repo}", f"--export-type=png", "--export-dpi=500"], capture_output=True, text=True, check=True)

def update_all_appendix_figures():
    all_svg_paths = get_files_with_extension("figures/appendix", "svg")
    for svg_path in all_svg_paths:
        pdf_path_repo = svg_path.replace("svg", "pdf")
        png_path_repo = svg_path.replace("svg", "png")
        pdf_path_dropbox = f"C:/Users/timod/Dropbox/Apps/Overleaf/MSc Thesis/Figures/" + svg_path.split("/")[-1].replace("svg", "pdf")
        a = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_repo}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        b = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_dropbox}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        c = subprocess.run(["inkscape", svg_path, f"--export-filename={png_path_repo}", f"--export-type=png", "--export-dpi=500"], capture_output=True, text=True, check=True)


def update_all_setup_figures():
    all_svg_paths = get_files_with_extension("figures/setup", "svg")
    for svg_path in all_svg_paths:
        pdf_path_repo = svg_path.replace("svg", "pdf")
        png_path_repo = svg_path.replace("svg", "png")
        pdf_path_dropbox = f"C:/Users/timod/Dropbox/Apps/Overleaf/MSc Thesis/Figures/" + svg_path.split("/")[-1].replace("svg", "pdf")
        a = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_repo}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        b = subprocess.run(["inkscape", svg_path, f"--export-filename={pdf_path_dropbox}", f"--export-type=pdf"], capture_output=True, text=True, check=True)
        c = subprocess.run(["inkscape", svg_path, f"--export-filename={png_path_repo}", f"--export-type=png", "--export-dpi=500"], capture_output=True, text=True, check=True)


def process_saturation_dataset(dataset: xr.Dataset) -> xr.Dataset:
    dataset["power_nw"] = dataset.power * W_TO_NW
    dataset.power_nw.attrs = {
        "units": "nW",
        "long_name": "Readout Power"
    }
    dataset = dataset.swap_dims({"power": "power_nw"})
    dataset["count_amplitude_khz"] = dataset.count_amplitude * HZ_TO_KHZ
    dataset.count_amplitude_khz.attrs = {
        "units": "kHz",
        "long_name": "Count rate"
    }
    dataset['decay_rate_khz'] = dataset.decay_rate * MHZ_TO_KHZ
    dataset.decay_rate_khz.attrs = {
        "units": "kHz",
        "long_name": "Decay rate"
    }

    dataset['timetrace_khz'] = dataset.timetrace * HZ_TO_KHZ
    dataset.timetrace_khz.attrs = {
        "units": "kHz",
        "long_name": "Count rate"
    }
    return dataset