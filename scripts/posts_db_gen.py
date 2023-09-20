import os

# This goofy little script was originally gonna be used to take a list of
# files, and spit out a nice and pretty array of JavaScript objects.

# I stopped caring about it cause I decided I wanted the next iteration of
# my site to be free of JavaScript. Doesn't really need it...

# OBSOLETE.

def tidyup(title):
    tidy_title = '\t\t"title": "' + title
    
    # Correct capitalisation of common character names
    tidy_title = tidy_title.replace("mull", "Müll")
    tidy_title = tidy_title.replace("muell", "Müll")
    tidy_title = tidy_title.replace("avril", "Avril")
    tidy_title = tidy_title.replace("dairy", "Dairy", 1) # Dairy the dairy cow
    tidy_title = tidy_title.replace("murbandictionary", "Mürbandictionary:")

    tidy_title += '",\n' # Close the string properly.

    return tidy_title


def scrape(filename):
    # Open a new array for this post, avoiding an additional comma for the first.
    if filenames.index(filename) == 0: post = '\n\t{\n'
    else: post = ',\n\t{\n'

    # Append the filename to the string.
    post += f'\t\t"images": ["{filename}"],\n'

    # Append the date to the string in YYYYMMDD format.
    post += f'\t\t"date": "{filename.split("-")[0]}",\n'

    # Pass the title argument into tidy-up function, append what's returned.
    post += tidyup(" ".join(filename.split("-")[1:]).split(".webp")[0])

    # Gleam any char attributes from filename, otherwise "muell" as default.
    if "avril" in filename: post += f'\t\t"chars": "avril",\n'
    elif "dairy" in filename: post += f'\t\t"chars": "dairy",\n'
    else: post += f'\t\t"chars": "muell",\n'

    # Append sane defaults for remaining variables where required.
    post += '\t\t"tags": [],\n' # Post tags
    post += '\t\t"licence": "CC0",\n' # Post licencing (nearly always CC0)
    post += '\t\t"desc": "",\n'
    post += '\t\t"transcript": ""\n'

    post += '\t}' # Close the string properly.

    return post


filenames = []
# Initialise a list holding all filenames in the "media" directory of PWD.
for entry in os.scandir('media'):
    if entry.is_file():
        filenames.append(entry.name)

# Open "posts.js" with UTF-8 encoding, overwriting any existing file.
with open("posts.js", "w", encoding='utf-8') as posts:
    # Open the "posts" array to hold the posts.
    posts.write('let posts = [')

    # Scrape each file we've got to prepare post entries.
    for filename in filenames:
        posts.write(scrape(filename))
    
    posts.write('\n]\n') # Finish off the file properly.
