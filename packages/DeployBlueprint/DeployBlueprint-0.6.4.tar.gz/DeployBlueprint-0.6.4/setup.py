from setuptools import *

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()
with open("readme.md", "r") as fh:
    long_description = fh.read()
with open("version.txt", "r") as fh:
    vers = fh.read().splitlines()[0]

setup(
	name='DeployBlueprint',
	version=vers,
	py_modules=['DeployBlueprint'],
	packages=find_packages(),
	install_requires=required,
	long_description=long_description,
    long_description_content_type="text/markdown",
	author="graboskyc",
	author_email="chris@grabosky.net",
	description="A basic tool to deploy AWS Instances and MongoDB Atlas Clusters for when using Cloud Formation, Terraform, Habitat, or others is overkill.",
    url="https://github.com/graboskyc/DeployBlueprint",
	entry_points='''
		[console_scripts]
		DeployBlueprint=DeployBlueprint:cli
	''',
)