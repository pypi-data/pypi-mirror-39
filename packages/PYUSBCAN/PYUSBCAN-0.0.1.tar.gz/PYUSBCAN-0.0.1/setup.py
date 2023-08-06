from setuptools import setup, find_packages

setup(
    name = "PYUSBCAN",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "USBCAN","ZLG"),
    description = "A Python tool to control zlg-usbcan",

    url = "https://github.com/fa1247/PYCAN",     #项目相关文件地址，一般是github
    author = "XY Fan",

    packages=find_packages(),
    python_requires='>=3',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.dll', '*.h', '*.lib']
    },
    platforms = "win",
    install_requires = ["ctypes"]          #这个项目需要的第三方库
)