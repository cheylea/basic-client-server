from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Client/Server Network',
    version='0.1.0',
    description='Basic client server for serialising and encrypting dictionaries and text files.',
    long_description=readme,
    author='Benjamin Barnes, Cheylea Hopkinson and Devin van Rooyen',
    author_email='B.Barnes@liverpool.ac.uk, C.Z.L.Hopkinson@liverpool.ac.uk, D.Van-Rooyen@liverpool.ac.uk',
    url='https://gitlab.csc.liv.ac.uk/sgchopk2/group-project-server',
    license=license,
)