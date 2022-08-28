from peewee import *

db = SqliteDatabase(r"DB\library.db")

class Category(Model):
    name = CharField()
    parent = IntegerField()
    
    class Meta:
        database = db 

class Location(Model):
    location = CharField(unique=True)
    class Meta:
        database = db 
      
class Publisher(Model):
    name = CharField(unique=True)
    location = ForeignKeyField(Location, backref='location_id', null=True)
    class Meta:
        database = db 

class Author(Model):
    name = CharField(unique=True)
    mail = CharField(null=True)
    class Meta:
        database = db 

BOOK_STATUS = (
    (1, 'New'),
    (2, 'Used'),
    (3, 'Old')
)

class Book(Model):
    
    
    title = CharField(unique=True)
    description = TextField(null=True)
    category = ForeignKeyField(Category, backref='category')
    code = CharField(null=True, unique=True)
    #parts = 
    part_order = IntegerField(null=True)
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher, backref='publisher', null=True)
    author = ForeignKeyField(Author, backref='author', null=True)
    image = CharField(null=True)
    status = CharField(choices=BOOK_STATUS)
    date = DateTimeField()
    class Meta:
        database = db 
    
class Clients(Model):
    
    name = CharField()
    mail = CharField(null=True, unique=True)
    phone = CharField(null=True)
    nat_id = IntegerField(unique=True)
    date = DateTimeField()
    class Meta:
        database = db 

class Employee(Model):
    nat_id = IntegerField(unique=True)
    name = CharField()
    mail = CharField(null=True, unique=True)
    phone = CharField(null=True)
    date = DateTimeField()
    periority = IntegerField()
    class Meta:
        database = db 
    

class Branch(Model):
    name = CharField()
    code = CharField(unique=True)
    location = ForeignKeyField(Location, backref='location_id', null=True)
    class Meta:
        database = db 
    
OPERATION = (
    (1, 'Borrow'),
    (2, 'Retrieve')
)
class DialyMovement(Model):
    book = ForeignKeyField(Book, backref='book')
    client = ForeignKeyField(Clients, backref='client')
    operation = CharField(choices=OPERATION)
    branch = ForeignKeyField(Branch, backref='branch')
    date = DateTimeField()
    from_date = DateTimeField()
    to_date = DateTimeField()
    employee = ForeignKeyField(Employee, backref='employee')
    class Meta:
        database = db 


ACTIONS = (
    (1, 'Login'),
    (2, 'Update'),
    (3, 'Create'),
    (4, 'Delete')
)

TABLES = (
    (1, 'Books'),
    (2, 'Clients'),
    (3, 'Employee'),
    (4, 'Category'),
    (5, 'Branch'),
    (6, 'Dialy Movement'),
    (7, 'Publisher'),
    (8, 'Author'),
)

class History(Model):
    employee = ForeignKeyField(Employee, backref='employee')
    action = CharField(choices=ACTIONS)
    table = CharField(choices=TABLES)
    date = DateTimeField()
    branch = ForeignKeyField(Branch, backref='branch')
    class Meta:
        database = db 

db.connect()
db.create_tables([Category, Location,Publisher, Author, Book, Clients, Employee, Branch, DialyMovement, History])