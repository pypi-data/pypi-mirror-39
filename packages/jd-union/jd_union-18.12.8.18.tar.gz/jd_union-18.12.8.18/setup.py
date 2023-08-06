# -*- coding: utf-8 -*-
# @Time    : 2018-12-08 17:09
# @Author  : play4fun
# @File    : setup.py
# @Software: PyCharm

"""
setup.py:
"""

from setuptools import setup, find_packages
print(find_packages())

setup(
    name='jd_union',
    version='18.12.8.18',  # 按日期
    author='play4fun',
    author_email='play4fun@foxmail.com',
    packages=find_packages(),
    # packages=['jd_union'],
    install_requires=[],
    license='MIT',
    description="京东联盟 sdk",
    long_description_content_type="text/markdown",
    long_description='京东联盟 sdk,进行导购推广,有了它，不需要去写爬虫抓取联盟商品信息'
)
