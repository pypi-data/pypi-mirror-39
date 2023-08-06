from setuptools import setup, find_packages

setup(
    name='teitoku',
    version='0.0.3',
    packages=find_packages(),
    author='yukinotenshi',
    author_email='gabriel.bentara@gmail.com',
    license='MIT',
    url='https://github.com/yukinotenshi/teitoku',
    install_requires=[],
    description='Write once for all chatbot framework',
    keywords='chatbot line telegram discord',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown"
)