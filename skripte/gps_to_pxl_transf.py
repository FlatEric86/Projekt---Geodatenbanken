import PY_lib, os, sys


lat, lon = float(sys.argv[1]), float(sys.argv[2])

try:
    px_x, px_y = PY_lib.GPS_to_PXL(lat, lon)
    print(str(px_x) + ';' + str(px_y))
except:
    print('ERRR')





