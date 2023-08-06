import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="DFYS_autodiff",
                 version="0.0.1",
                 author="Feiyu Chen; Yueting Luo; Yan Zhao",
                 author_email="yluo@hsph.harvard.edu",
                 description="An automatic differentiation package",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/pypi/DFYS-autodiff",
                 packages=setuptools.find_packages(),
                 classifiers=[
                              "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
