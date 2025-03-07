FROM python:3.10-alpine

WORKDIR /app
RUN apk add g++ libc-dev hdf5-dev linux-headers
# ENV HDF5_DIR=/usr/lib
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/data
COPY . .

# RUN ./get_data.sh
# RUN ./build_index.sh
