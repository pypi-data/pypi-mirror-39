import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='stx-tools',
    packages=setuptools.find_packages(),
    version='0.0.3',
    description='Nuestra "Navaja suiza" con clases de python que nos '
                'ayudan a crear rápidamente nuestros proyectos.',
    author='Carlos A. Martínez Jiménez',
    author_email='carloxdev@gmail.com',
    url='https://github.com/carloxdev/stx-tools',
    download_url='https://github.com/carloxdev/stx-tools/tarball/0.1',
    keywords=['archivos', 'python', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
