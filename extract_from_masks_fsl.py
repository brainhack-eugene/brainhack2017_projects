from nilearn.masking import apply_mask
import nibabel as nib
import nilearn
import os.path as op

def extract_from_masks(mask_files,data_file,masknames=None):
    #given a data file and a set of mask files, extract timeseries from the data 
    #for each mask. Returns a dictionary with the key corresponding to the mask
    #(derived from the file name) and the value as a numpy array that's TR x voxels
    
    output = [apply_mask(data_file,m) for m in mask_files] 
    
    if mask_files[0] is str:    
        masknames = [op.splitext(op.splitext(op.basename(x))[0])[0] for x in mask_files]

    if masknames is not None:
            output = dict(zip(masknames,output))

    return(output) 

def generate_masks(atlas_image, therange = None):
    
    atlas_img = nib.load(atlas_image)
    labeled_image_data = atlas_img.get_data()

    if therange == None:
        therange = range(labeled_image_data.min(), labeled_image_data.max()+1)
    masks = list()
    for i in range(len(therange)):

        tempmask = nilearn.image.new_img_like(atlas_image,labeled_image_data==therange[i])
        masks.append(tempmask)

    return(masks)