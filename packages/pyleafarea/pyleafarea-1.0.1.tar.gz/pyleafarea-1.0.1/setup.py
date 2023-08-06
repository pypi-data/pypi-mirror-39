from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE.txt", "r") as fh:
    lic = fh.read()

setup(
    name='pyleafarea',
    version='1.0.1',
    packages=['pyleaf'],
    url='',
    license=lic,
    long_description=long_description,
    install_requires=[
        'Keras>=2.2.4',
        'numpy>=1.15.2',
        'pandas>=0.23.0',
        'Pillow>=5.3.0',
        'tensorflow'],
    tests_require=["pytest"],
    include_package_data=True,
    author='Vishal Sonawane',
    author_email='vishalsonawane1515@gmail.com',
    description='Automated Leaf Area Calculator Using Tkinter and Deep Learning Image Classification Model.'
)