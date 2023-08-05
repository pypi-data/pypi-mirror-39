#encoding:UTF-8
#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

setup(
    name='wq_setup_demo',               #'<项目的名称>'
    version='1.0.9.dev1',
    description='测试打包上传pip',        #'<项目的简单描述>'
    url='https://github.com/13126655557/wq_pyspider.git',  #'<项目的网址，我一般都是github的url>'
    author='wangquan',                  #'<你的名字>',
    author_email='13126655557@163.com', #'<你的邮件地址>'
    #packages=['wq_pypi_demo'],         #可以通过名字制定要打的包名
    packages=find_packages(),    #find_packages()默认在和setup.py同一目录下搜索各个含有__init__.py的包。
                                 #find_packages('src'),     包含setup同级目录下，自定义src文件夹中所有的包
    #find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])  排除一些特定的包，如果在src中再增加一个tests包，可以通过exclude来排除它,
    #package_dir = {'':'src'},     #告诉distutils包都在src下
                                 #另外，这个包内可能还有aaa.txt文件和data数据文件夹。'''
    # package_data={
    #     # 任何包中含有.txt文件，都包含它
    #     '': ['*.txt'],
    #     # 包含demo包data文件夹中的 *.dat文件
    #     'demo': ['data/*.dat'],
    # },
    #intclude_package_data=True,    # 启用清单文件MANIFEST.in  清单文件作用与package_data类似可以自定义包含哪些资源文件
    #exclude_package_date={'':['.gitignore']}       排除哪类资源文件比如readme
    license='MIT',
    install_requires=[  # 依赖包下载路径
        "beautifulsoup4",           #pip install beautifulsoup4
        'Flask>=0.10',              #自动安装xxx lib 并制定版本号
        'Flask-SQLAlchemy>=1.5,<=2.1'
    ],
    dependency_links=[  # 依赖包下载路径  install_requires中无法下载的话自动去下面的网址下载
        'http://example.com/dependency.tar.gz'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='wq project python',

)

#https://blog.csdn.net/pfm685757/article/details/48651389
#http://python.jobbole.com/87240/


#检查setup文件配置 输出一般是running check
#python setup.py check
#开始使用Distutils进行打包
#python setup.py sdist
#执行完成后，会在顶层目录下生成dist目录和egg目录
#python setup.py

#python setup.py register sdist upload
#Wqq2596489!


