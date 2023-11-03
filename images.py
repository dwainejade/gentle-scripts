
import os

# accepts index of the page, as well as interactive name and dirpath 
# returns images dict (object) for that page

# can use on title, readalong, and hot text pages. 

# Does not support feedback character images at this time
def map_paths(ix_of_page, interactive_name, dirpath):
    # if images exist, they will be found here
    instructional = "%s/%s/images/%s_page%s_inst.png" %(dirpath, interactive_name, interactive_name, ix_of_page)
    border = "%s/%s/images/%s_page0_border.png" %(dirpath, interactive_name, interactive_name)
    instructional_jpg = "%s/%s/images/%s_page%s_inst.jpg" %(dirpath, interactive_name, interactive_name, ix_of_page)
    border_jpg = "%s/%s/images/%s_page%s_border.jpg" %(dirpath, interactive_name, interactive_name, ix_of_page)
   

    paths = [instructional, border, instructional_jpg, border_jpg]
    # trim the path string to include relative path in images dict (object)
    starting_ix = len("%s/%s/" % (dirpath, interactive_name))
    images = {
     
        "borderImg": "",
        "instructionalImg": "",
        "instructionalImgAlt": "",
        "instructionalImgCaption": ""
    }

    for i in range(len(paths)):
        # if image exists, add it to images
        if os.path.isfile(paths[i]):
            relative_img_path = str(paths[i])[starting_ix:]
            if paths[i] == instructional_jpg or paths[i] == instructional:
                images["instructionalImg"] = relative_img_path
            elif paths[i] == border_jpg or paths[i] == border:
                images["borderImg"] = relative_img_path
    
    # remove unused properties
    properties_to_delete = []

    for key, value in images.items():
        if value == "":
            properties_to_delete.append(key)
    
    if len(properties_to_delete) > 0:
        for i in range(len(properties_to_delete)):
            property_to_delete = properties_to_delete[i]
            del images[property_to_delete]


    return images


# Future direction: if we agree to convert jpg images to png, remove jpg paths
# Alternatively, if we end up having to support more image file types, add more
# paths 
#
# ADD SUPPORT FOR INSTRUCTIONALIMGCAPTION, so that we don't have to do it manually
# 
# At some point, perhaps when we are working with different feedback characters
# based on feedback type in hot text pages, expand this function to support 
# mapping custom character images as well.    