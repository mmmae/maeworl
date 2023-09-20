import os
from PIL import Image

# This script is to be run inside a directory of originals.
# OBSOLETE. remake and repurpose for use within hochladen.

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files[:-1]:
    print('..', f)
    
    with Image.open(f) as im:
        im.thumbnail((420, 420))
        im.save('thumbs/' + f)
