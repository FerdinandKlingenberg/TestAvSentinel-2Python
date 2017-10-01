import sys,os,time,glob,shutil,re,multiprocessing, errno
from distutils.dir_util import copy_tree
#with open('/media/fklingenberg/Expansion Drive/HentGranules/GranuleListe.csv', 'rb') as f:
#    reader = csv.reader(f)
#    your_list = list(reader)

#print your_list
#your_list2 = map(str,your_list)
#print your_list2

#your_list3 = []

#for i in your_list2:
#	your_list3.append(i.replace('['


# Read list with Granules which should be used 
GranuleList = open('/media/fklingenberg/Expansion Drive/HentGranules/GranuleListe.csv').read().splitlines()

#print GranuleList

#Path where your list of granules will be saved
newpath = '/media/fklingenberg/Expansion Drive/HentGranules/NewData/'

# Initalize list of granules with full path
granuleFilepathstring = ''

# Create single granule folders if not exist
for i in GranuleList:
	granuleFilepathstring = newpath+i
	print(granuleFilepathstring)
	if not os.path.exists(granuleFilepathstring):
		os.makedirs(granuleFilepathstring)

granuleFilePathList = glob.glob(newpath + '/*')
#print granuleFilePathList

# Path where your Sentinel-2 data exist, assuming their are unzipped before
s2DataPath = '/media/fklingenberg/Expansion Drive/HentGranules/Data'
# List of Sentinel-2 data which data should be extracted from
s2DataListe = glob.glob(s2DataPath + '/*')
#print s2DataListe


fc_list = glob.glob(s2DataPath+'/*/GRANULE/*/')
#print fc_list

# Initalize string of copy location
copyTooLocation = ''
nameS2A_OPER = 'S2A_OPER'

#Credits to https://stackoverflow.com/a/3368991
def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ''

def find_between_r( s, first, last ):
	try:
		start = s.rindex( first ) + len( first )
		end = s.rindex( last, start )
		return s[start:end]
	except ValueError:
		return ''


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


t1 = ''
t2 = ''
t3 = ''

for x in GranuleList:
	for y in fc_list:
		if y.endswith(x+'/'):
			print x
			print('og ')
			print y
			print('og filepath ')
			
			#File will be saved in this folder
			copyTooLocation = newpath + x
			(filepath, filename) = os.path.split(y)
			print filepath
			print('og filename ')
			print filename
			print ('og soeking: ')
			betweenF = find_between(y,'S2A_OPER','.SAFE')
			nameS2A_OPER = copyTooLocation + '/S2A_OPER' + betweenF + '.SAFE'
			if not os.path.exists(nameS2A_OPER):
				os.makedirs(nameS2A_OPER)
			
			t1 = s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/AUX_DATA'
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE/AUX_DATA'
			print t1
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			copy_tree(t1, t3)
			
			t1 = s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/DATASTRIP'
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE/DATASTRIP'
			print t1
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			copy_tree(t1, t3)
			
			
			###############
			betweenGranule = find_between(y,'_MSI_L1C_','N02.04')
			t4 = s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/GRANULE/S2A_OPER_MSI_L1C_' + betweenGranule + 'N02.04'
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE/GRANULE'
			t5 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE/GRANULE/S2A_OPER_MSI_L1C_' + betweenGranule + 'N02.04'
			print t1
			print t2
			
			if not os.path.exists(t2):
				os.makedirs(t2)
			if not os.path.exists(t5):
				os.makedirs(t5)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t6 = t4 #+ '/'
			t7 = t5 + '/'
			copy_tree(t4, t7)
			#print t5
			#print betweenGranule
			############
						



			t1 = s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/HTML'
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE/HTML'
			print t1
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			copy_tree(t1, t3)
			
			t1 = s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/rep_info'
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE/rep_info'
			print t1
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			copy_tree(t1, t3)
			
			
			t1 = glob.glob(s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/INSPIRE.xml')
			strTemp = ''.join(t1)
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE'
			print t1
			print strTemp
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			shutil.copy2(strTemp, t3)

			t1 = glob.glob(s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/*.safe')
			strTemp = ''.join(t1)
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE'
			print t1
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			shutil.copy2(strTemp, t3)
			
			
			t1 = glob.glob(s2DataPath + '/S2A_OPER' + betweenF +'.SAFE/S2A*.xml')
			strTemp = ''.join(t1)
			t2 = copyTooLocation + '/S2A_OPER' + betweenF +'.SAFE'
			print t1
			print t2
			if not os.path.exists(t2):
				os.makedirs(t2)
			#shutil.copytree(t1, t2)
			#copytree(t1,t2)
			t3 = t2 + '/'
			shutil.copy2(strTemp, t3)








#for longfilename in fc_list:
#	if any (x in longfilename for x in GranuleList):
#		if any (y in longfilename for y in granuleFilePathList):
#			print longfilename

		
		
		
    #(filepath, filename) = os.path.split(name)
    #outName = glob.glob(filepath+"\\GRANULE\*\\S2A*.xml")
    #strTemp = ''.join(outName)

    ## Change end of filename with correct file extention
    #(filepath, filename) = os.path.split(strTemp)
    #OutputImage = filepathresultat+"\\"+filename[:-4]+"_10m.pix"


#for i in s2DataListe:
#	if any (x in (glob.glob(i+'/GRANULE/*/IMG_DATA/')) for x in GranuleList:
#		print i
