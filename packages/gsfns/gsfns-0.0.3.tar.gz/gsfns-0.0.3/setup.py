import setuptools

with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(name='gsfns',
                 version='0.0.3',
                 author ='datnt',
                 author_email = 'nguyentiendat@dongguk.edu',
                 description  = 'General Support Functions',
                 long_description=long_description,
                 long_description_content_type = "text/markdown",
                 packages=setuptools.find_packages(),
                 classifiers=["Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                 ])
