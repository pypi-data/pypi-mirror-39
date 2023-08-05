from setuptools import setup, find_packages

setup(
    name='pythonframework',
    version='0.0.3',
    keywords=('pyframework',),
    description='pyframework powerd by lanceyan.com',
    license='MIT License',
    install_requires=[],
    packages=find_packages(exclude=[  'tests']),
    include_package_data=True,
    author='lanceyan',
    author_email='lanceyan@vip.qq.com',
    url='https://github.com/lanceyan/pyframework',
    # packages = find_packages(include=("*"),),
)
