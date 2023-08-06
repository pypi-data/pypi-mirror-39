"""Example script to search metadata for data from one
Austalk speaker and download all of their digit data.

To run this script you need to install the pyalveo library
which is available at (https://pypi.python.org/pypi/pyalveo/0.4) for
installation with the normal Python package tools (pip install pyalveo).

You also need to download your API key (alveo.config) from the Alveo web application
(click on your email address at the top right) and save it in your home directory:

Linux or Unix: /home/<user>
Mac: /Users/<user>
Windows: C:\\Users\\<user>

The script should then find this file and access Alveo on your behalf.



 """
from __future__ import print_function
import os
import pyalveo

item_list_name = 'over-50-hvd'

# directory to write downloaded data into
outputdir = "data"

client = pyalveo.Client(use_cache=False)

itemlist = client.get_item_list_by_name(item_list_name)

if not os.path.exists(outputdir):
    os.makedirs(outputdir)

for itemurl in itemlist:
    item = client.get_item(itemurl)
    meta = item.metadata()

    speakerurl = meta['alveo:metadata']['olac:speaker']
    speaker_meta = client.get_speaker(speakerurl)
    speakerid = speaker_meta['dcterms:identifier']

    # write out to a subdirectory based on the speaker identifier
    subdir = os.path.join(outputdir, speakerid)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    for doc in item.get_documents():
        filename = doc.get_filename()

        if filename.endswith('speaker16.wav') or filename.endswith('.TextGrid'):
            print(filename)
            doc.download_content(dir_path=subdir)


