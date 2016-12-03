软件打包方法：
=========================================================
py2exe:        python setup.py py2exe

pyinstaller:   pyinstaller -F -w -i icon.ico weiClient.py
			   pyinstaller -F -c -p C:\Python27; -i icon.ico appServer.py

