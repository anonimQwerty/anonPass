from sqlalchemy import Table, Column, Integer, LargeBinary
def create_struckture(name, meta):
	struck = Table(
   name, meta, 
   Column('id', Integer, primary_key = True), 
   Column('user', LargeBinary), 
   Column('passw', LargeBinary), 
   Column('url', LargeBinary), 
   Column('comment', LargeBinary))	
	return struck