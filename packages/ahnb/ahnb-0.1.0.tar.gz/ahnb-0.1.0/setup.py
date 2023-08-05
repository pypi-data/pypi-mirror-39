import setuptools

authors = "Andrew McNutt, Will Brackenbury, Ahsan Pervaiz"
description = "A callback library which submits model and training statistics to AHNB"

setuptools.setup(name="ahnb",
                 version="0.1.0",
                 author=authors,
                 description=description,
                 long_description=description,
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent"])
