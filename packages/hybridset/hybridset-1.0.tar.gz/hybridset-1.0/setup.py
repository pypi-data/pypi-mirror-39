from setuptools import setup


package_name = "hybridset"
version = '1.0'
url = 'https://gitlab.com/yahya-abou-imran/hybridset'
url_fmt = '/-/archive/v{version}/archive.zip/{package_name}-v{version}.zip'
download_url = (
    url + url_fmt.format(version=version, package_name=package_name)
)
description=('Mutable set storing apart hashables and unhashables values')
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


setup(
    name=package_name,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    author='Yahya Abou Imran',
    author_email='yahya-abou-imran@pm.me',
    license='GPLv3',
    url=url,
    download_url=download_url,
    packages=[package_name],
)
