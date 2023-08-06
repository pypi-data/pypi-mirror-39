from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='colabo.flow.go',
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.2.1',
    url='https://github.com/Cha-OS/colabo',
    # download_url,
    project_urls={
        'website': 'http://colabo.space',
        'organization': 'http://cha-os.org'
    },
    author='ChaOS',
    author_email='chaos.ngo@gmail.com',
    license='MIT',
    description='A python puzzle for sending ColaboFlow.Go (CF.Go) actions over gRPC',
    keywords=['colabo','grpc','flow','colaboflow', 'go', 'process', 'process mining'],
    packages=find_packages(),
    # requires=['grpcio', 'googleapis-common-protos', 'python-dateutil'],
    install_requires=['grpcio', 'googleapis-common-protos', 'python-dateutil']
)
