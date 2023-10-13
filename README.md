## maeworl

The source for [maeworl.xyz](https://maeworl.xyz). Included are some scripts and templates I use to make development easier.


#### /www

The website itself. Pretty much all images aren't included, for obvious reasons... Refer to /.gitignore for details, and to adjust the exclusion/inclusions as required.

#### /scripts
Houses a couple handy python scripts for necessary bulk operations and housekeeping. These are specific to my needs, but you're free to repurpose them however you want. Hochladen is a simple GUI application that simplifies uploads to the neocities WebDAV of maeworl.xyz.


Hochladen *intends to* do the following:
- Uploads the original file to the appropriate directory.
- Uploads a generated thumbnail to the appropriate directory.
- Adds a new entry to archive.html, complete with associated metadata, and updates the Atom feed accordingly.
