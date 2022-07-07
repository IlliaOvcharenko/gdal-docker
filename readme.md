# 🐳 GDAL Dockerfile (with ECW format and Python support)
[![DockerHub](https://img.shields.io/docker/cloud/build/indigoilya/gdal-docker?style=flat-square)](https://hub.docker.com/r/indigoilya/gdal-docker)

base on ubuntu:18.04

## How to run?

### Installation
```
docker pull indigoilya/gdal-docker
```

### Convert ecw to geotiff
Command to convert a folder with ecw to geotiff
```
docker run -v /path/to/files:/data -v /path/to/output:/data_output indigoilya/gdal-docker python /home/scripts/converter.py --input_folder=/data --output_folder=/data_output --out_format=geotiff
```

Supported output formats:
- geotiff
- tif
- npy
- png

### Help / Information
Script is using Fire (command line interface generator)
```
docker run indigoilya/gdal-docker python /home/scripts/converter.py --help
```
