# FROM python-image
FROM ubuntu:18.04

# Install Miniconda with Python 3.7
ARG PYTHON_VERSION=3.7
ARG WITH_TORCHVISION=1
RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         ca-certificates \
         libjpeg-dev \
         libpng-dev && \
     rm -rf /var/lib/apt/lists/*

RUN curl -o ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION && \
     rm ~/miniconda.sh && \
     /opt/conda/bin/conda clean -ya
ENV PATH /opt/conda/bin:$PATH


# Install ECW driver
RUN apt update && DEBIAN_FRONTEND="noninteractive" apt -y install tzdata
RUN apt update \
    && apt install -y zip \
    && apt install -y expect
COPY ./install-ecw-sdk.exp ./install-ecw-sdk.exp

RUN curl -L -o erdas-ecw-sdk-5.4.0-linux.zip http://go.hexagongeospatial.com/ERDASECW/JP2SDKv.5.4Linux \
    && unzip erdas-ecw-sdk-5.4.0-linux.zip \
    && chmod +x ERDAS_ECWJP2_SDK-5.4.0.bin\
    && expect ./install-ecw-sdk.exp \
    && cp -r /hexagon/ERDAS-ECW_JPEG_2000_SDK-5.4.0/Desktop_Read-Only /usr/local/hexagon \
    && rm -r /usr/local/hexagon/lib/x64 \
    && mv /usr/local/hexagon/lib/newabi/x64 /usr/local/hexagon/lib/x64 \
    && cp /usr/local/hexagon/lib/x64/release/libNCSEcw* /usr/local/lib \
    && ldconfig /usr/local/hexagon \
    && rm erdas-ecw-sdk-5.4.0-linux.zip \
    && rm ERDAS_ECWJP2_SDK-5.4.0.bin \
    && rm install-ecw-sdk.exp


# Install GDAL 2.3.1
RUN curl -L -o gdal231.zip http://download.osgeo.org/gdal/2.3.1/gdal231.zip \
    && unzip gdal231.zip \
    && cd gdal-2.3.1 \
    && ./configure --with-ecw=/usr/local/hexagon --with-python \
    && make clean \
    && make \
    && make install \
    && cd .. \
    && rm gdal231.zip \
    && ldconfig


# Install pip dependencies
RUN pip install numpy==1.19.1
RUN pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
RUN pip install fire==0.3.1
RUN pip install tqdm==4.46.0
RUN pip install Pillow==7.2.0

# Copy scripts
WORKDIR /home
COPY ./npy_to_img.py ./scripts/npy_to_img.py
COPY ./ecw_to_npy.py ./scripts/ecw_to_npy.py
