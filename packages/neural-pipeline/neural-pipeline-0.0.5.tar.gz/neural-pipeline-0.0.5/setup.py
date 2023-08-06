import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neural-pipeline",
    version="0.0.5",
    author="Anton Fedotov",
    author_email="anton.fedotov.af@gmail.com.com",
    description="Neural Networks train pipeline based on PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toodef/neural-pipeline",
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=['numpy', 'tensorboardX', 'tqdm', 'torch==0.4.1'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
