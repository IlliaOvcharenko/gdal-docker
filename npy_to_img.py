import numpy as np

from PIL import Image
from pathlib import Path
from fire import Fire
from tqdm.cli import tqdm

def main(data_folder="data"):
    data_folder = Path(data_folder)
    filenames = list(data_folder.glob("*.npy"))
    for fn in tqdm(filenames, desc="plot img"):
        img = np.load(fn)
        img = Image.fromarray(img)
        img.save(fn.with_suffix(".png"))

if __name__ == '__main__':
    Fire(main)
