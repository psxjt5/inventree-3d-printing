# -*- coding: utf-8 -*-

import importlib
import importlib.util
import os
import setuptools

"""Read the plugin version from the source code."""
module_path = os.path.join(
    os.path.dirname(__file__), "inventree_3d", "__init__.py"
)
spec = importlib.util.spec_from_file_location("inventree_3d", module_path)
inventree_3d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventree_3d)

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-3d-printing",
    version=inventree_3d.PLUGIN_VERSION,
    author="James Todd",
    author_email="james.todd@nottingham.ac.uk",
    description="3D Printing Support for InvenTree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="inventree 3d printer printing inventory",
    url="https://github.com/psxjt5/inventree-3d-printing",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[],
    setup_requires=[
        "wheel",
        "twine",
    ],
    python_requires=">=3.9",
    entry_points={
        "inventree_plugins": [
            "3DPrinting = inventree_3d.threed_plugin:ThreeDPlugin"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: InvenTree",
    ],
)
