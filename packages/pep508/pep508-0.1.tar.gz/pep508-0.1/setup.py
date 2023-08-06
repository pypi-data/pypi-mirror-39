import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pep508",
    version="0.1",
    author="Kristian Glass",
    author_email="pep508@doismellburning.co.uk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doismellburning/pep508",
    packages=setuptools.find_packages(),
    py_modules=["pep508"],
    package_dir={"": "src"},
    license="MPL v2",
)
