import importlib.util

banner = """ __         __
/  \.-\"\"\"-./  \\
\    -   -    /
 |   o   o   |
 \  .-'''-.  /
  '-\__Y__/-'
     `---`
"""

if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location(
        'code', 'code.cpython-37.pyc')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print(banner)
    flag = input("Enter passpharse: ").strip()
    print('Yes, flag is Flag{%s}' % flag if mod.check_flag(flag) else 'No!')
