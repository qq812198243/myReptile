#!F:\pycharmProjects\gufengdongman\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'slimit==0.8.1','console_scripts','slimit'
__requires__ = 'slimit==0.8.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('slimit==0.8.1', 'console_scripts', 'slimit')()
    )
