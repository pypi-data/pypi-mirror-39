from setuptools import setup, find_packages

setup(name='nlutools',\
                version='1.10.0',\
                description='introduction information for nlu tools',\
                long_description=open('README.md').read(),\
                url='https://github.com',\
                author='LH19880520',\
                author_email='huan.liu@ifchange.com',\
                license='ifchange',\
                install_requires=['requests>=2.18.4'],\
                packages=find_packages(),\
                include_package_data=True,\
                zip_safe=False)




