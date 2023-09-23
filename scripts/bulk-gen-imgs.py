import os
from PIL import Image

# This script is to be run inside a directory of originals.
# OBSOLETE. remake and repurpose for use within hochladen.

files = [f for f in os.listdir('.') if os.path.isfile(f)]

files.reverse()

for f in files:
    print(f'<div class="item"><a href="/img/archive/{f}"><img src="/img/archive/thumbs/{f}" alt="thumbnail" loading="lazy"></a><div class="lice" title="CC0"></div></div>')
