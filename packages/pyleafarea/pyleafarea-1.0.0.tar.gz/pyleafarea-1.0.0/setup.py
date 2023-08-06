from setuptools import setup

setup(
    name='pyleafarea',
    version='1.0.0',
    packages=['pyleaf'],
    url='',
    license='',
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