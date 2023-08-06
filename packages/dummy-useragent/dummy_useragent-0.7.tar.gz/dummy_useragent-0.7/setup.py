import setuptools

setuptools.setup(
    name="dummy_useragent",
    version="0.7",
    description="random useragent without network",
    long_description="",
    author="Hexmagic",
    packages=setuptools.find_packages(),
    include_package_data=True,
    author_email="191440042@qq.com",
    url="https://github.com/Hexmagic/dummy_useragent.git",
    license="GNU General Public License v3.0",
    install_requires=["aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
)
