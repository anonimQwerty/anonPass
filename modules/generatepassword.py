import random
def generatepassword(mode, lenght):
	passw=""
	chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
	numbers="1234567890"
	specialchars="!@#$%^&*()_-+=/<>?:;"

	if mode==1:
		for i in range(lenght):
			passw+=random.choice(chars)

	if mode==2:
		for i in range(lenght):
			passw+=random.choice(numbers)

	if mode==3:
		for i in range(lenght):
			passw+=random.choice(specialchars)

	if mode==4:
		for i in range(lenght):
			passw+=random.choice(chars+numbers)

	if mode==5:
		for i in range(lenght):
			passw+=random.choice(chars+specialchars)

	if mode==6:
		for i in range(lenght):
			passw+=random.choice(numbers+specialchars)


	if mode==7:
		for i in range(lenght):
			passw+=random.choice(chars+numbers+specialchars)


	return passw