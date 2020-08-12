import cv2
import gdal

import numpy as np

from pathlib import Path
from fire import Fire
from tqdm.cli import tqdm

def gdal_imread(filename, return_geotransform=True):
    filename = str(filename)
    ds = gdal.Open(filename)
    geotransform = ds.GetGeoTransform()
    channels_num = ds.RasterCount
    img = None

    if channels_num == 1:
        img = ds.GetRasterBand(1).ReadAsArray()
    else:
        channels = [ds.GetRasterBand(i).ReadAsArray() for i in range(1, channels_num+1)]
        img = np.stack(channels, axis=2)

    if return_geotransform:
        return img, geotransform
    return img

def to_geotiff(img, save_filename, geotransform):
    nx = img.shape[1]
    ny = img.shape[0]
    dst_ds = gdal.GetDriverByName('GTiff').Create(str(save_filename), nx, ny, 3, gdal.GDT_Byte)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.GetRasterBand(1).WriteArray(img[:, :, 0])
    dst_ds.GetRasterBand(2).WriteArray(img[:, :, 1])
    dst_ds.GetRasterBand(3).WriteArray(img[:, :, 2])
    dst_ds.FlushCache()
    dst_ds = None

def create_binding_file(out_img_filename, geotransform):
    xoff, a, b, yoff, d, e  = geotransform
    out_img_ext = out_img_filename.suffix.replace(".", "")
    binding_ext = f".{out_img_ext[0]}{out_img_ext[-1]}w"
    binding_filename = out_img_filename.with_suffix(binding_ext)
    with open(binding_filename, "w") as f:
        for value in [a, b, d, e, xoff, yoff]:
            f.write(f"{value}\n")

def main(input_folder="data", output_folder="data", out_format="tif", create_binding=False):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    filenames = list(input_folder.glob("*.ecw"))
    for fn in filenames:
        img, geotransform = gdal_imread(fn)
        img = img[:,:,:3]


        if out_format == "tif":
            out_img_filename = (output_folder / fn.name).with_suffix(".tif")
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(out_img_filename), img)

        elif out_format == "geotiff":
            out_img_filename = (output_folder / fn.name).with_suffix(".tif")
            to_geotiff(img, out_img_filename, geotransform)

        elif out_format == "npy":
            out_img_filename = (output_folder / fn.name).with_suffix(".npy")
            np.save(out_img_filename, img)

        elif out_format == "png":
            out_img_filename = (output_folder / fn.name).with_suffix(".png")
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(out_img_filename), img)

        if create_binding:
            create_binding_file(out_img_filename, geotransform)

        print(out_img_filename)


if __name__ == '__main__':
    Fire(main)