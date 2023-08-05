import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='clinphen',
    version='1.18',
    #scripts=['clinphen','get_phenotypes.py', 'prep_thesaurus.py', 'umls_thesaurus_extraction.sh', 'clinphen_setup.sh', 'src/hpo_names.py', 'src/hpo_syns.py', 'src/standardize_syn_map.py', 'data/common_phenotypes.txt'],
    scripts=['clinphen'],
    author="Cole A. Deisseroth",
    author_email="cdeisser@stanford.edu",
    description="An automatic phenotype extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://bejerano.stanford.edu/clinphen/",
    packages=setuptools.find_packages() + ['clinphen_src'],
    include_package_data=True,
    install_requires=['nltk'],
     classifiers=[
         "Programming Language :: Python :: 2.7",
         "Operating System :: OS Independent",
     ],
 )

