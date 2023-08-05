from dal import Simpledal


db = Simpledal()

db.insert(a=1, b=2)
print(vars(db))

db.delete('a')
print(vars(db))

db.update(c=3)
print(vars(db))

val = db.get('b')
print (val)

db2 = Simpledal()
print(vars(db2))

