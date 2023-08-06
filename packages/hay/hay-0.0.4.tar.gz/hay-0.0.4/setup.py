import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode("utf8")

setuptools.setup(
    name="hay",
    version="0.0.4",
    description='基于pyppeteer的chromenium操控库',
    author='白旭东,储国庆',
    author_email='2216403312@qq.com',
    license="BSD",
    url='https://github.com/oldlwhite/hay',
    include_package_data = True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)


