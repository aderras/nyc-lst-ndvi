import os
import rioxarray as rxr

def get_filenames(starting_dir, names):
    """
    This function recursively searches starting_dir for all
    files in the deepest level of the main folder. It appends
    filenames to the input variable, names, a 1d list. 

    in: starting_dir = "string", names = 1d list. 
    out: returns nothing, but appends to "names" input var     
    """
    
    contents = os.listdir(starting_dir)
    for c in contents:
        if os.path.isdir(starting_dir +"/" + c):
            get_filenames(starting_dir + "/" + c, names)
        else:
            names.append(starting_dir + "/"+ c)
            
def open_and_clip(filepath, boundary):
    """
        Open a .tif file and immediately clip it to a boundary. This is used to clip Landsat
        files to NYC. 
    """
    
    xds = rxr.open_rasterio(filepath)
    clipped = xds.rio.clip(boundary.geometry.values, boundary.crs)

    return clipped.squeeze()

def clip_and_export(rawfilepath, boundary, outfilepath):
    """
        Open and export a clipped file
    """
    clipped_file = open_and_clip(rawfilepath, boundary)
    clipped_file.rio.to_raster(outfilepath)