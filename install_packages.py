packages=['requests','fake_headers','multiprocessing','datetime','time','logging','os','flask','threading','importlib']

import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

for package in packages:
    import_or_install(package)