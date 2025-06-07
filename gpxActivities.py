from transfer import *
from parselatlon import *
from pathlib import Path

print('Put all your .gpx files in the "data" directory.')
directory = Path('data')
gpx_files = list(directory.glob('*.gpx'))
gpx_files = [str(f) for f in directory.glob('*.gpx')]
print('These are all .gpx files in the directory:')
for i in range(len(gpx_files)):
	print(str(i)+'\t'+gpx_files[i])
print('The index of the .gpx file in the above list (0-base), and the number of similar routes to plot:')
index, K=input().split(' ')
index, K=int(index), int(K)
paintpath([parseGpx(i) for i in gpx_files], index, K)
