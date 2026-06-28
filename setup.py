from setuptools import setup, find_packages

setup(
    name="aiosofascore",
    version="0.1.3.0",
    description="API client for SofaScore soccer data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Philip",
    author_email="vasilewskij.fil@gmail.com",
    url="https://github.com/Rooney27/aio_sofascore",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiohttp",
        "pydantic"
    ],
    python_requires='>=3.10',  # Укажите минимальную версию Python
)