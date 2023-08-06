import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="DFYS_autodiff",
                 version="1.0.0",
                 author="Feiyu Chen; Yueting Luo; Yan Zhao",
                 author_email="yluo@hsph.harvard.edu",
                 description="An automatic differentiation package",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/D-F-Y-S/cs207-FinalProject",
                 packages=setuptools.find_packages(),
                 classifiers=[
                              "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
