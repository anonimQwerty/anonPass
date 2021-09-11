def check_version():

	with open('version.txt', 'r', encoding='utf-8') as f:
		version_nums=f.readline().split('.')
	return version_nums