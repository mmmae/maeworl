import os

# This script is to be run inside a directory of originals.
# OBSOLETE. remake and repurpose for a new version of the site.

counter = 0
for entry in os.scandir('.'):
    if entry.is_file():
        print('posts[' + str(counter) + '] = [\'' + entry.name + '\', \'' + ' '.join(entry.name.split("-")[1:]).replace(".webp", "") + '\', \'tags\', \'mull\', \'cc0\', \'desc\', \'\'];')
        counter = counter + 1