from setuptools import setup, find_packages

setup(
    name='colour_to_dmc',
    extras_require=dict(tests=['pytest', 'scipy', 'opencv-python', 'pandas', 'numpy', 'matplotlib']),
    packages=find_packages(where='src'),
    package_dir={"": "src"},

)
