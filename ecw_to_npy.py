import gdal

import numpy as np

from pathlib import Path
from fire import Fire
from tqdm.cli import tqdm

def gdal_imread(filename):
    filename = str(filename)
    ds = gdal.Open(filename)

    channels_num = ds.RasterCount

    if channels_num == 1:
        return ds.GetRasterBand(1).ReadAsArray()
    else:
        channels = [ds.GetRasterBand(i)for i in range(1, channels_num+1)]
        channels = [ch.ReadAsArray() for ch in channels]
        return np.stack(channels, axis=2)


# def main(filename, to_rgb=True):
#     # filename = "data/Mbombela_2021.ecw"
#     img = gdal_imread(filename)

#     if to_rgb:
#         img = img[:,:,:3]
#     print(img.shape)


def main(data_folder="data", to_rgb=True):
    data_folder = Path(data_folder)
    filenames = list(data_folder.glob("*.ecw"))
    for fn in tqdm(filenames, desc="convert img"):
        img = gdal_imread(fn)
        img = img[:,:,:3] if to_rgb else img
        np.save(fn.with_suffix(".npy"), img)


if __name__ == '__main__':
    Fire(main)
