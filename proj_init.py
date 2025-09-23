import os
try:
    os.system("python -m pip install -r requirements.txt")
    with open('.env', 'w', encoding='utf-8') as fenv:
        root = os.getcwd()
        fenv.write('ROOT='+ root + '\n')
        fenv.close()
    print('Successfully inited.')
except:
    print('Error while initing system.')
