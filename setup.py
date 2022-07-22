from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name="otscannerlibs",
  version="1.0.0",
  description='Images/Creds Python Libraries',
  author='Abhishek Kumar Tiwari',
  author_email='abhishek.tiwari@opstree.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=["otscannerlibs"],
  python_requires=">=3.6",
)
