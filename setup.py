from setuptools import setup, find_packages

setup(
    name="ErnieBot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "customtkinter~=5.1.3",
        "openai~=0.27.6",
        "gradio~=3.30.0",
        "Pillow~=9.5.0",
        "setuptools~=65.5.1",
    ],
)
