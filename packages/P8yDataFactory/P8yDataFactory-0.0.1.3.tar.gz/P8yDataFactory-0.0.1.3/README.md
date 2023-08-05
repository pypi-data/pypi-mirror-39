sdist             create a source distribution (tarball, zip file, etc.) 
bdist             create a built (binary) distribution 
bdist_dumb        create a "dumb" built distribution 
bdist_rpm         create an RPM distribution 
bdist_wininst     create an executable installer for MS Windows 
bdist_egg         create an "egg" distribution


pip install twine
# 上传package
python setup.py sdist　#生成的文件支持 pip 
twine upload dist/* 

文件：
~/.pypirc
  1 [distutils]
  2 index-servers=pypi
  3
  4 [pypi]
  5 repository = https://upload.pypi.org/legacy/
  6 username = tywldx
  7 password = Tyw12345*