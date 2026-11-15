import py_compile

with open('RR_EDGE_Dashboard/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'elif page == "16. RR-EDGE V4.2 Franchise Decision Intelligence Command Centre":'
idx = text.find(target)
if idx != -1:
    code = text[idx:]
    with open('RR_EDGE_V3_0/dashboard/app.py', 'r', encoding='utf-8') as f:
        v3_text = f.read()
    if target not in v3_text:
        v3_text = v3_text.rstrip() + '\n\n' + code
        with open('RR_EDGE_V3_0/dashboard/app.py', 'w', encoding='utf-8') as f:
            f.write(v3_text)
        print("Successfully synced Console 16 to RR_EDGE_V3_0/dashboard/app.py")
    else:
        print("Already present in RR_EDGE_V3_0")

py_compile.compile('RR_EDGE_Dashboard/app.py', doraise=True)
py_compile.compile('RR_EDGE_V3_0/dashboard/app.py', doraise=True)
print("Both dashboard apps compiled cleanly with 0 syntax errors!")
