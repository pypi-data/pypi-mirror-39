import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
version = next((row.split('=', 1)[-1].strip().strip("'").strip('"')
                for row in open('iptcinfo3.py', 'r')
                if row.startswith('__version__')))
setuptools.setup(
    name="IPTCInfo3",
    version=version,
    author='Tamas Gulacsi',
    author_email='gthomas@fw.hu',
    maintainer='James Campbell',
    maintainer_email='james@jamescampbell.us',
    description="IPTC info for images in Python 3",
    license='http://www.opensource.org/licenses/gpl-license.php',
    platforms=['any'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamesacampbell/iptcinfo3",
    packages=setuptools.find_packages(),
    keywords="iptc image-metadata metadata",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Artistic License",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities"
    ],
    py_modules=['iptcinfo3'],
    python_requires='>=3',
)
