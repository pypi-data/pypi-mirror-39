from setuptools import setup
import weightwatcher as ww

import io
with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name = ww.__name__,
    version = ww.__version__,
    url = ww.__url__,
    project_urls={
        "Documentation": "https://calculationconsulting.com/",
        "Code": "https://github.com/calculatedcontent/weightwatcher",
        "Issue tracker": "https://github.com/calculationconsulting/weightwatcher/issues",
    },
    license = ww.__license__,
    author = ww.__author__,
    author_email = ww.__email__,
    maintainer = ww.__author__,
    maintainer_email = ww.__email__,
    description = ww.__description__,
    long_description = readme,
    long_description_content_type = "text/markdown",
    packages = ["weightwatcher"],
    include_package_data = True,
    python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires = ['numpy',
                        'matplotlib',
                        'powerlaw',
                        'tensorflow',
                        'keras',
                        'sklearn'],
    entry_points = '''
        [console_scripts]
        weightwatcher=weightwatcher:main
    ''',
    classifiersi = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
	"Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords = "Deep Learning Keras Tensorflow pytorch CNN DNN Neural Networks",
)
