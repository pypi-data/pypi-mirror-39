from setuptools import setup, find_packages

setup(
    name='AILog',
    version='1.0.4',
    description='Library that provides configurable colored and formatted logging with sane defaults',
    url='http://github.com/ai-systems/AILog',
    author='AI Systems, University of Manchester',
    author_email='viktor.schlegel@manchester.ac.uk',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    package_data={"ailog": ["resources/*"]},
    include_package_data=True,
    install_requires=["aiconf", "colorlog"],
)
