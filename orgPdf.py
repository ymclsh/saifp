import os
import re
import shutil

def orgFiles(orgRoot):
	print os.listdir(orgRoot)

	for root, dirs, files in os.walk(orgRoot):
		splitfilenames = [file.split('_') for file in files]

		while True:
			try:
				current = []
				current.append(splitfilenames.pop())
				code = current[0][0]
				year = current[0][1]
				postfix = current[0][2]

				for splits in splitfilenames:
					if splits[0] == code and splits[1] == year and splits[2] != postfix :
						current += [splits]

				for i in current[1:]:
					splitfilenames.remove(i)

				moveFiles(root, current)

			except IndexError: #pop from empty list
				break

def moveFiles(root, namelists):
	leng = len(namelists)

	if leng == 1 :
		#move to [year] fold direct
		moveFile(root, namelists[0][0], namelists[0][1], namelists[0][2], True, False)
		print namelists

	if leng == 2:
		#move to [year] or [year_full] folder based on the file size
		statinfo_1 = os.stat(root + namelists[0][0] +'_'+ namelists[0][1] + '_' + namelists[0][2])
		statinfo_2 = os.stat(root + namelists[1][0] +'_'+ namelists[1][1] + '_' + namelists[1][2])
		if statinfo_1.st_size > statinfo_2.st_size: #[0] is full disclosure, [1] is brief
			moveFile(root, namelists[0][0], namelists[0][1], namelists[0][2], True, False)
			moveFile(root, namelists[1][0], namelists[1][1], namelists[1][2], False, False)
		else:
			moveFile(root, namelists[0][0], namelists[0][1], namelists[0][2], False, False)
			moveFile(root, namelists[1][0], namelists[1][1], namelists[1][2], True, False)

		
	else:
		#even there is exception, assume the biggest size is the full disclosure version
		biggest = []
		size = 0

		#find out the full disclosure version
		for file in namelists:
			path = root + file[0] + '_' + file[1] + '_' + file[2]
			statinfo = os.stat(path)
			if statinfo.st_size > size:
				size = statinfo.st_size
				biggest = file
		if size != 0 :
			moveFile(root, biggest[0], biggest[1], biggest[2], True, False)
			namelists.remove(biggest)

		while True:
			try:
				current = []
				current = namelists.pop()
				code = current[0]
				year = current[1]
				postfix = current[2]
				moveFile(root, code, year, postfix, False, True)
			except IndexError:
				break

def moveFile(root, code, year, postfix, isFullDisclosure, isException):

	name = code + '_'  + year + '_' + postfix
	tofolder = getFolder(root, year, isFullDisclosure, isException)
	topath = tofolder + '/' + name

	frompath =root + name

	shutil.move(frompath, tofolder)


def getFolder(root, year, isFullDisclosure, isException):

	if True == isException :
		path = root + 'Exception'
	else:
		if True == isFullDisclosure :
			path = root +year+'_full'
		else :
			path =  root + year
	if False == os.path.exists(path):
		os.makedirs(path)
	return path



if __name__ == '__main__':

	orgFiles("C:\\_workshop\\prj_saif_paper\\pdfs\\")


