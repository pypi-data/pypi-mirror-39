import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='spjson',  
     version='0.2',
     #scripts=['spjson.py'] ,
     author="Shankar Prasad",
     author_email="ishankar.prasad@gmail.com",
     description="Nested JSON to CSV parser",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/shankarpd/spjson",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )