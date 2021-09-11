import pyaes, hashlib, random, os
from requests import Session, get
from sqlalchemy import MetaData, Table, Column, Integer, String, LargeBinary, create_engine, insert, inspect, delete, update, text
from sqlalchemy.orm import sessionmaker

from modules.logo import logo
from modules.check_version import check_version
from modules.ShredFile import ShredFile
from modules.generatepassword import generatepassword
from modules.create_struckture import create_struckture



def check_new_version(server='https://raw.githubusercontent.com/anonimQwerty/anonPass/master/version.txt'):
	r=get(server)
	if r.status_code==200:
		new_version=r.text.split('.')
		return new_version


	else:
		print("something went wrong")

def show_changelog(server='https://raw.githubusercontent.com/anonimQwerty/anonPass/master/changelog.txt'):
	r=get(server)
	if r.status_code==200:
		changelog=r.text
		return changelog


	else:
		print("something went wrong")


def check_for_updates(position=0):
	new_version=check_new_version()
	old_version=check_version()
	if int(new_version[position])>int(old_version[position]):
		print('The new version is aviable. If you have a git on your pc, you can update it')
		changelog=int(input('Can I show changelog? 1-yes, 2-no: '))
		if changelog==1:
			print(show_changelog())
		does_update=int(input('\n\n\nDo you wanna to update it? 1-yes, 2-no: '))
		if does_update==1:
			os.system('git pull')

	elif position==2:
		print('No updates')
	else:
		position+=1
		check_for_updates(position)
	







def str_aes_crypt(stri, pas):
	aes = pyaes.AESModeOfOperationCTR(pas)
	ciphertext = aes.encrypt(stri)
	return ciphertext

def str_aes_decrypt(stri, pas):
	aes = pyaes.AESModeOfOperationCTR(pas)
	ciphertext = aes.decrypt(stri)
	return ciphertext

def gensalt(password, salt):

	key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('utf-8'), 100000, dklen=32)
	return key

def aescrypt(file1, file2, key):
	# Create the mode of operation to encrypt with
	mode = pyaes.AESModeOfOperationCTR(key)

	# The input and output files
	file_in = open(file1, 'rb')
	file_out = open(file2, 'wb')

	# Encrypt the data as a stream, the file is read in 8kb chunks, be default
	pyaes.encrypt_stream(mode, file_in, file_out)

	# Close the files
	file_in.close()
	file_out.close()


def aesdecrypt(file1, file2, key):
	# Create the mode of operation to encrypt with
	mode = pyaes.AESModeOfOperationCTR(key)

	# The input and output files
	file_in = open(file1, 'rb')
	file_out = open(file2, 'wb')

	# Encrypt the data as a stream, the file is read in 8kb chunks, be default
	pyaes.decrypt_stream(mode, file_in, file_out)

	# Close the files
	file_in.close()
	file_out.close()






def master_of_creation_passwords():
	amount=int(input('Input amount chars in your password: '))
	mode=int(input('''
						Select one from this modes:
1: chars only
2: numbers only
3: specialcars only
4: chars + numbers
5: chars + specialchars
6: numbers + specialchars
7: chars + numbers + specialchars: '''))
	while True:
		password=generatepassword(mode, amount)
		print(f'You password is {password}. Is this password ok? 1-yes, 2-no, 3-cancel')
		result_there=int(input())
		if result_there==1:
			return password
			break
		elif result_there==3:
			password=''
			return password
			break







logo()
check_for_updates()
startcommand=int(input('1. Create database\n2. Open database\n3. Check for updates\n4. Watch changelog: '))
if startcommand==1:
	db_name=input('\nSet name for database: ')
	db_password=input('\nSet password for database: ')
	record_pass=input('\nSet password for records: ')
	

	doescreatekeyfordb=int(input('\nCreate key for database? 1-yes 2-no. \nWarning if you lost your key, you can\'t open your database in future: '))
	doescreatekeyforrecords=int(input('\nCreate key for records? 1-yes 2-no. \nWarning if you lost your key, you can\'t open your database in future: '))


	with open('key.salt_key', 'w') as f:
		salt=generatepassword(7, 256)
		f.write(salt)
		print('File with salt has saved. Warning if you lost your key, you can\'t open your database in future')

	if doescreatekeyforrecords==1:
		key=generatepassword(7, 32)
		#print(key)

		with open('key.rec_key', 'w') as f:
			f.write(key)
		test=str_aes_crypt('test_data', key.encode('utf-8'))
		test=str_aes_crypt(test, gensalt(record_pass, salt))
	
	engine = create_engine(f'sqlite:///{db_name}.ass', echo = True)
	meta = MetaData()
	first_table=create_struckture('accounts', meta)
	meta.create_all(engine)
	cursor=engine.connect()
	
	
	if doescreatekeyforrecords==2:
		test=str_aes_crypt('test_data', gensalt(record_pass, salt))
	print(test)
	cursor.execute(insert(first_table).values(user=test, passw=test, url=test, comment=test))
	cursor.close()
	

	m=gensalt(db_password, salt)
	

	aescrypt((f'{db_name}.ass'), (f'{db_name}1.ass'), m)


	if doescreatekeyfordb==1:
		key=generatepassword(7, 32)
		aescrypt((f'{db_name}1.ass'), (f'{db_name}.ass'), key.encode('utf-8'))

		ShredFile(f'{db_name}1.ass')
		with open('key.db_key', 'w') as f:
			f.write(key)


	

	
	if doescreatekeyfordb!=1:
		ShredFile(f'{db_name}.ass')
		os.rename(f'{db_name}1.ass', f'{db_name}.ass')
		
		

elif startcommand==3:
	check_for_updates()



elif startcommand==4:
	print(show_changelog())


else:


	#aesdecrypt('qwerty.ass', 'qwerty1.ass', r"o:=*Bp*I%oK5Swpk/%Jg4O3kQ)!:d9k1".encode('utf-8'))

	#qw=gensalt('qwe', "wq:>!ZJ>o>Nba7DC&nkOZe&>>fIg1Xd%5q5w<3(J%!;aZLxL6z1B2bdOaV$4IF_eCV4v?Cw(_FxBsbz:-X;:^Unq!B3C>#m4joAF>gSWAF5#I9BIOCufc+;Y>-K<xXvxMvin=16dI5wIPD^4q;yo6SDh5j6xy/BDtxR21U#@22:Jgez:pF/uCO;i#KGy9%TPMp!pJ^9<#ne/a;(r1$3%yke^cvxvx2WreR:aVsMFXw5uAZIz^nQLM;:e==-d95xE")
	#print(qw)
	#aesdecrypt('qwerty1.ass', 'qwerty2.ass', qw)

	db_name=input('\nEnter name for database (without .ass): ')
	db_name+='.ass'
	db_password=input('\nEnter password for database: ')
	record_pass=input('\nEnter password for records: ')

	salt_file=input('Name file with salt: ')
	salt_file+='.salt_key'

	

	doescreatedkeyfordb=int(input('\nHave you created key for database? 1-yes 2-no.: '))
	doescreatedkeyforrecords=int(input('\nHave you created key for records? 1-yes 2-no: '))

	if doescreatedkeyfordb==1:
		db_key=input('Type name for key of db. Important: this key must be in same folder with script!!: ')
		db_key+='.db_key'
		tempvar=open(db_key, 'r')
		
		db_key=tempvar.readline().encode('utf-8')
		tempvar.close()


	if doescreatedkeyforrecords==1:
		rec_key=input('Type name for key of records(with extenstion). Important: this key must be in same folder with script!!: ')
		rec_key+='.rec_key'
		tempvar=open(rec_key, 'r')
		rec_key=tempvar.readline().encode('utf-8')
		tempvar.close()


	tempvar=open(salt_file, 'r')
	salt_key=tempvar.readline()
	tempvar.close()
	

	name_decrypted_db=generatepassword(1, 7)+'.'+generatepassword(1, 3)
	tempname=generatepassword(1,7)+'.'+generatepassword(1, 3)

	if doescreatedkeyfordb==1:
		aesdecrypt(db_name, tempname, db_key)
		aesdecrypt(tempname, name_decrypted_db, gensalt(db_password, salt_key))
		ShredFile(tempname)

	elif doescreatedkeyfordb==2:
		aesdecrypt(db_name, name_decrypted_db, gensalt(db_password, salt_key))




	engine = create_engine(f'sqlite:///{name_decrypted_db}', echo = False)
	meta = MetaData()
	inspector=inspect(engine)
	connection=engine.connect()
	session=sessionmaker(engine)
	session=session()


	logo()

	print("Connected to db. \nWelcome, master")
	changes_in_db=False
	
	while True:
		print("""		List of commands:
1: List of tables
q: exit
t: Create table""")
		command=input('Type command:')
		try:

			if command=='1':
				for table in range(len(inspector.get_table_names())):
					
					print(table, inspector.get_table_names()[table])

				select_table=input("""Type number table, which you want to open

d: delete table
q: back to menu: """)
				if select_table=='q':
					continue

				elif select_table=='d':
					num_table=int(input('Type number of table: '))
					print(select_table)
					select_table_backup=select_table

					select_table=num_table

					select_table=inspector.get_table_names()[select_table]
					print(select_table)

						
					select_table=create_struckture(select_table, meta)

					select_table.drop(engine)

					inspector = inspect(engine)
					changes_in_db=True



				else:
					while True:
						print(select_table)
						select_table_backup=select_table
						select_table=int(select_table)
						
						select_table=inspector.get_table_names()[select_table]
						print(select_table)

						
						select_table=create_struckture(select_table, meta)
						

						rows=connection.execute(select_table.select())
						for i in rows:
							username=i[1]
							password=i[2]
							url=i[3]
							comment=i[4]

							if doescreatedkeyforrecords==1:
								
								username=str_aes_decrypt(username, gensalt(record_pass, salt_key))
								username=str_aes_decrypt(username, rec_key).decode('utf-8')

								
								password=str_aes_decrypt(password, gensalt(record_pass, salt_key))
								password=str_aes_decrypt(password, rec_key).decode('utf-8')

								
								url=str_aes_decrypt(url, gensalt(record_pass, salt_key))
								url=str_aes_decrypt(url, rec_key).decode('utf-8')

								
								comment=str_aes_decrypt(comment, gensalt(record_pass, salt_key))
								comment=str_aes_decrypt(comment, rec_key).decode('utf-8')


							else:
								username=str_aes_decrypt(username, gensalt(record_pass, salt_key)).decode('utf-8')
								password=str_aes_decrypt(password, gensalt(record_pass, salt_key)).decode('utf-8')
								url=str_aes_decrypt(url, gensalt(record_pass, salt_key)).decode('utf-8')
								comment=str_aes_decrypt(comment, gensalt(record_pass, salt_key)).decode('utf-8')
								
							print(f'Id: {i[0]}, username: {username}, password: {password}, url: {url}, comment: {comment}')


						result=input("""
c: create record
d: delete record
e: edit record
q: back to main menu: """)
						if result=='c':
							username=input('Enter username: ')
							password=input('Enter password(leave 4 spases to generate password): ')

							if password=='    ':	
								password=master_of_creation_passwords()
							url=input('Enter url: ')
							comment=input('Enter comment: ')

							

							if doescreatedkeyforrecords==1:
								username=str_aes_crypt(username, rec_key)
								password=str_aes_crypt(password, rec_key)
								url=str_aes_crypt(url, rec_key)
								comment=str_aes_crypt(comment, rec_key)



							username=str_aes_crypt(username, gensalt(record_pass, salt_key))
							password=str_aes_crypt(password, gensalt(record_pass, salt_key))
							url=str_aes_crypt(url, gensalt(record_pass, salt_key))
							comment=str_aes_crypt(comment, gensalt(record_pass, salt_key))


							connection.execute(insert(select_table).values(user=username, passw=password, url=url, comment=comment))
							changes_in_db=True

						elif result=='d':
							rec_id=int(input('Enter id record: '))
							connection.execute(delete(select_table).where(select_table.c.id==rec_id))
							changes_in_db=True
							del(rec_id)



						elif result=='e':
							rec_id=input('Enter id record: ')
							#print(inspector.get_table_names()[select_table_backup])
							#print(type(select_table_backup))
							username_backup = username
							password_backup = password
							url_backup = url
							comment_backup = comment

							username=input('Enter new username. If you dont want change, leave 2 spaces: ')
							if username=='  ':
								username=username_backup

							password=input('Enter new password. If you dont want change, leave this field empty. If you wanna to generate password, leave 4 spaces. If you dont want change, leave 2 spaces: ')
							if password=='    ':	
								password=master_of_creation_passwords()
							elif password=='  ':
								password=password_backup

							url=input('Enter new url. If you dont want change, leave 2 spaces: ')
							if url=='  ':
								url=url_backup
							comment=input('Enter new comment. If you dont want change, leave 2 spaces: ')
							if comment=='  ':
								comment=comment_backup

							if doescreatedkeyforrecords==1:
								username=str_aes_crypt(username, rec_key)
								password=str_aes_crypt(password, rec_key)
								url=str_aes_crypt(url, rec_key)
								comment=str_aes_crypt(comment, rec_key)


							username=str_aes_crypt(username, gensalt(record_pass, salt_key))
							password=str_aes_crypt(password, gensalt(record_pass, salt_key))
							url=str_aes_crypt(url, gensalt(record_pass, salt_key))
							comment=str_aes_crypt(comment, gensalt(record_pass, salt_key))


							connection.execute(select_table.update().where(select_table.c.id==rec_id).values(user=username, passw=password, url=url, comment=comment))

							changes_in_db=True
							del(rec_id)


						elif result=='q':
							break
						del(meta, password, username, url, comment)
						meta = MetaData()
						select_table=select_table_backup

			elif command=='t':
				tablename=input('Enter table name: ')
				stucture=create_struckture(tablename, meta)
				meta.create_all(engine)
				changes_in_db=True
				inspector=inspect(engine)
				del(tablename)
				del(stucture)









					
		except Exception as e:
			raise e
			#print('Something went wrong') db_name

		if command=='q':
			connection.close()
			if changes_in_db:
				ShredFile(db_name)
				aescrypt(name_decrypted_db, f'{db_name}1', gensalt(db_password, salt_key))
				if doescreatedkeyfordb==1:
					aescrypt(f'{db_name}1', (f'{db_name}'), db_key)

					ShredFile(f'{db_name}1')


	

	
				if doescreatedkeyfordb!=1:
					os.rename(f'{db_name}1', f'{db_name}')
				ShredFile(name_decrypted_db)
				break

			else:
				ShredFile(name_decrypted_db)
				break

		del(meta)
		meta = MetaData()