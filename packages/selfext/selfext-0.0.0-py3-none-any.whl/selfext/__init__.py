#!/usr/bin/env python3
#coding: utf-8

from base64 import b85encode
from glob import glob
from zipfile import ZipFile
from random import choice

from tempfile import mkdtemp
from os.path import join, basename
from os import remove

sample = """
#!/usr/bin/env python3
#coding: utf-8

from base64 import b85decode
from zipfile import ZipFile
from os import remove

fn = "FILENAME"

def main(DATA):
    with open(fn, "wb") as fp:
        fp.write(b85decode(DATA.replace(b"\n", b"")))
    with ZipFile(fn) as zip:
        zip.extractall(".")
    remove(fn)

DATA = b\"\"\"
ENCODED_DATA
\"\"\"

if __name__ == "__main__":
    main(DATA)
"""

def encode(path):
    with open(path, "rb") as f:
        DATA = f.read()
    DATA = b85encode(DATA)
    DATA = str(DATA)[2:-1]
    DATA = '\n'.join([DATA[i: i+80] for i in range(0, len(DATA), 80)])
    return DATA

def make_extfile(path, output_fn):
    global sample
    DATA = encode(path)
    sample = sample.replace("ENCODED_DATA", DATA)
    sample = sample.replace("FILENAME", basename(path[2:]))
    with open(output_fn, "w") as f:
        f.write(sample)

def make_zip(compdir):
    global zippath
    zippath = mkdtemp()+".zip"
    with ZipFile(zippath, 'w') as new_zip:
        if compdir[-1] != "/":
            compdir += "/"
        for x in glob(compdir+"*"):
            new_zip.write(x, arcname=x)

def gen(compdir='./', outfile="Ext.py"):
    make_zip(compdir=compdir)
    make_extfile(path=zippath, output_fn=outfile)
    remove(zippath)

if __name__ == "__main__":
    gen()
    # remove("Ext.py")