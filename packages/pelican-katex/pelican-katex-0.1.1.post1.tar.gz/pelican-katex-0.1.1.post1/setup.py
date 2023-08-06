from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pelican-katex",
    version="0.1.1.post1",
    author="Marten Lienen",
    author_email="marten.lienen@gmail.com",
    description="Server-side LaTeX compilation for pelican",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cqql/pelican-katex",
    py_modules=["pelican_katex"],
    install_requires=["pelican", "docutils"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Framework :: Pelican :: Plugins"
    ])
