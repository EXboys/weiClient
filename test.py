# -*- coding: utf-8 -*-

import subprocess
try:
    subprocess.call('taskkill /f /t /im appServer.exe')
except Exception,e:
    pass

subprocess.call('./appServer.exe')