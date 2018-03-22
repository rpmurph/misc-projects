import os, sys
import gdal
import numpy

def read_file(file_name):
    ''' opens a raster and returns the dataset
        along with the area of each cell based
        on the pixel dimensions

        filename:: file path to the raster dataset
    '''

    # open the file
    file_handle = gdal.Open(file_name)

    # reads the first band of the raster dataset
    band1 = file_handle.GetRasterBand(1)
    band1_data = band1.ReadAsArray()
    geotransform = file_handle.GetGeoTransform()

    # close the file
    file_handle = None

    # get the x,y cell sizes in the layer units
    pixel_width = abs(geotransform[1]) 
    pixel_height = abs(geotransform[5]) 

    # print metadata and return
    return band1_data, (pixel_width * pixel_height)

def get_areas_by_zone(input_file, output_file, threshold=0):
    ''' processes a given raster dataset to get
        a long-form summary of the area (in the
        same units as the dataset) summariezed
        by unique raster value or "zone"

        input_file::    file path to the input raster dataset
        output_file::   file path for the summary output file
        threshold::     threshold value to ignore during processing
    '''

    # read file and extract the dataset
    # get pixel size in layer units
    the_data, xy_size = read_file(input_file)

    # set a minimum value threshold
    # NOTE: this is still a working idea, so
    #       leave set as the default for now
    the_data[ the_data < threshold ] = 0

    # get unique elements of the dataset
    my_set = numpy.unique( the_data )
    my_set = numpy.append(my_set, [numpy.amax(my_set)+1])

    # create histogram of the unique key values
    good_stuff = numpy.histogram( a=the_data, bins=my_set )

    # write histogram to file
    f = open(output_file, 'w')
    f.write('BIN,COUNT\n')

    # loop through unique values and write data in long-form
    for i in range(0, len(my_set)-1):
        f.write( str(long( good_stuff[1][i] )) + ',' + str(long( good_stuff[0][i] ) * xy_size) + '\n' )

    # close the output stream
    f.close()
