'''
Checkea que los archivos de empresa no tengan filas repetidas.
'''

import argparse


parser = argparse.ArgumentParser(description='Checkea que los archivos de empresa no tengan filas repetidas.')
parser.add_argument('filename', type=str,
                    help='Nombre del archivo a checkear')

args = parser.parse_args()




def check(filename):
    repeated = False
    readed = set()
    with open(filename, 'r') as file:
        for line in (line.strip() for line in file.readlines()):
            if line and not line.startswith('#'):
                if line in readed:
                    print("Repetido:", line)
                    repeated = True
                else:
                    readed.add(line)
    return repeated


if __name__ == "__main__":
    repeated = check(args.filename)
    if not repeated:
        print("No hay repetidos!")