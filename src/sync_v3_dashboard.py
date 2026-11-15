import sys
import os
import py_compile

with open('RR_EDGE_V3_0/dashboard/app.py', 'r', encoding='utf-8') as f:
    c = f.read()

sys.path.append('src')
from append_console_17_to_dashboard import CONSOLE_17_CODE

if 'page == "17. RR-EDGE Advanced Analytical Intelligence Suite' not in c:
    c = c.rstrip() + '\n' + CONSOLE_17_CODE
    with open('RR_EDGE_V3_0/dashboard/app.py', 'w', encoding='utf-8') as f:
        f.write(c)

py_compile.compile('RR_EDGE_V3_0/dashboard/app.py', doraise=True)
print('V3_0 compiled cleanly with 0 errors!')
