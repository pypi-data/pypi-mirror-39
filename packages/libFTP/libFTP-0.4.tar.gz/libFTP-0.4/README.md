# libFTP
## Install Pip
```
pip install -i https://test.pypi.org/simple/ libFTP
```
## Exmaple libFTP
```
import libFTP as lfp
lfp.Get("locahost","user account","password","dir","type","save")
```
>```localhost``` is **IP** for ftpserver.

>```user account``` is **user account** for ftpserver .

>```password``` is *** password account** for ftpserver .

>```dir``` is **Path folder get file** for ftpserver .

>```type``` is **Type file filter file get** for ftpserver .

>```save``` is **Path save file in localhost** from ftpserver .

* function lfp.Get can ```retrun True``` is Connect success. if ```retrun False``` is disconnect or Connect false.
