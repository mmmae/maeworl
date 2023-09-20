import os
import sys
import tempfile

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk

from PIL import Image, ImageOps
from webdav3.client import Client

if len(sys.argv) < 4: exit() # I'm not going to dignify that with a response.

# WebDAV client vars and options, default paths
local_images = 'D:/MEGA/art/exports/'
local_thumbs = tempfile.gettempdir() + '/hochladen/'
remote_images = '/media/archive/'
remote_thumbs = '/media/archive/thumbs/'

webdav_opts = {
    'disable_check': True,
    'webdav_timeout': 15,
    'webdav_hostname': sys.argv[1],
    'webdav_login': sys.argv[2],
    'webdav_password': sys.argv[3]
}
webdav_client = Client(webdav_opts)

def select_files():
    """
        Handles selection of image files with tkinter filedialog.
        Triggered only, not to be called manually.
    """
    files = fd.askopenfilenames(
        title='Select images to post',
        initialdir=local_images,
        filetypes=[('WebP Image','*.webp')]
    )

    # only act on filedialog use if the user has selected 1 or more files.
    if len(files) > 0:
        listbox_files.delete(0, "end")

        for f in files:
            listbox_files.insert("end", f)

def submit():
    """
        Handles submission of post, accompanying images, and info.
        Triggered only, not to be called manually.
    """
    # basic field validation before we continue
    if (len(entry_title.get()) == 0 or
        len(listbox_files.get(0, 'end')) == 0 or
        len(entry_tags.get()) == 0 or
        len(entry_chars.get()) == 0 or
        len(combobox_licence.get()) == 0):
            msgbox.showerror("Submission failed", "Some required " \
                    "fields are missing or have invalid input.")
            return

    # use PIL to create square thumbnails of images, store in %TEMP%
    for f in listbox_files.get(0, 'end'):
        with Image.open(f) as img:
            filename = f.split('/')[-1]

            thumb = ImageOps.fit(img, (360,360), centering=(0.5, 0.5),
                    bleed=0.1, method=Image.Resampling.LANCZOS)
            
            # save thumbnails in temp directory (create if doesn't exist)
            os.makedirs(os.path.dirname(local_thumbs + filename),
                exist_ok=True)
            thumb.save(local_thumbs + filename)

    # connect to WebDAV and upload images and their associated thumbnails
    try:
        for img in listbox_files.get(0, 'end'):
            filename = img.split('/')[-1]

            # first we upload the original images...
            webdav_client.upload_sync(
                    remote_path=remote_images + filename,
                    local_path=img)
            # then we upload the thumbnails...
            webdav_client.upload_sync(
                    remote_path=remote_thumbs + filename,
                    local_path=local_thumbs + filename)
    except:
        msgbox.showerror("Submission failed", "Unable to upload. " \
                "Confirm your WebDAV settings are correct, that the " \
                "host is reachable and files are valid.")
        return

    # add the post to the posts database
    # update the RSS feed with a new article

    msgbox_submit = msgbox.showinfo("Submitted!", "Seems everything " \
            "went OK! The post should now be on the homepage, in the RSS" \
            " feed, and in the archive.")

#############################################################################

root = tk.Tk()
root.title(f'Posting to {sys.argv[1]} as {sys.argv[2]}')
root.geometry('480x720')
root.resizable(False, False)

# instantiate all tkinter widgets
label_title = ttk.Label(text='Title *')
entry_title = ttk.Entry(width=40)

label_files = ttk.Label(text='Image(s) *')
listbox_files = tk.Listbox(width=50, height=5)
button_browse = ttk.Button(text='Browse...', command=select_files)

label_desc = ttk.Label(text='Description (inside a paragraph block)')
text_desc = tk.Text(width=50, height=9, wrap='word')

label_transcript = ttk.Label(text='Transcript (for translations)')
text_transcript = tk.Text(width=50, height=4, wrap='word')

label_tags = ttk.Label(text='Tags (space separated with dashes) *')
entry_tags = ttk.Entry(width=40)

label_chars = ttk.Label(text='Characters (space separated, romanised) *')
entry_chars = ttk.Entry(width=40)

licence = tk.StringVar()

label_licence = ttk.Label(text='Licence *')
combobox_licence = ttk.Combobox(textvariable=licence, width=5)
combobox_licence['values'] = ('CC0', 'ARR')

button_submit = ttk.Button(text='Submit', command=submit)

label_about = ttk.Label(foreground='grey',
        text= 'hochladen -- post submission client for maeworl.xyz')

# then, pack and position the widgets in the window
label_title.pack(pady=(8,4))
entry_title.pack()

label_files.pack(pady=(8,4))
listbox_files.pack()

button_browse.pack(pady=(4,4))

label_desc.pack(pady=(8,4))
text_desc.pack()

label_transcript.pack(pady=(8,4))
text_transcript.pack()

label_tags.pack(pady=(12,4))
entry_tags.pack()

label_chars.pack(pady=(8,4))
entry_chars.pack()

label_licence.pack(pady=(8,4))
combobox_licence.pack()

button_submit.pack(pady=(20,4))

label_about.pack(side='bottom', pady=(0,4))

root.mainloop()