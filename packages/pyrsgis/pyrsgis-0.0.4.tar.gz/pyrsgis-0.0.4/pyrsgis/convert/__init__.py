#convert
#pyrsgis

import os, glob
import numpy as np
import gdal
import csv

def rastertocsv(directory, filename='PyRSGIS_rasterToCSV.csv'):
    os.chdir(directory)

    data = []
    names = []
    for raster in glob.glob("*.tif"):
        names.append(raster[:-4])
        data.append(readRaster(raster))

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(names)
        for row in range(0,data[0].shape[0]):
            rowData = []
            for d in data:
                rowData.append(d[row][0])
            writer.writerow(rowData)

