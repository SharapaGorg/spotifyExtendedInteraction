import os, sys

def load_package(command):
    os.system(
        'cd \"' + os.path.dirname(sys.executable) + '\" && ' + os.path.basename(sys.executable) + ' -m ' + command
    )

with open('requirements.txt', 'r') as read_stream:
    for row in read_stream.readlines():
        load_package('pip install ' + row.rstrip('\n'))

