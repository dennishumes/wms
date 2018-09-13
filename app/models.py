

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
	"""
	Create a Department table
	"""

	__tablename__ = 'departments'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	users = db.relationship('User',  backref='department',lazy='dynamic')
	
	def __repr__(self):
		return '<Department: {}>'.format(self.name)



class Warehouse(db.Model):
	"""
		Create a Bin table
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(250))
	location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
	
	bins = db.relationship('Bin', backref='warehouse', lazy='dynamic')
	
	def __repr__(self):
		return '<Warehouse: {}>'.format(self.name)

class Bin(db.Model):
	"""
		Create a Bin table
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	depth = db.Column(db.Integer)
	warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
	

	def __repr__(self):
		return '<Bin: {}>'.format(self.name)


class Location(db.Model):
	"""
		Create a Location table
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))

	def __repr__(self):
		return '<Location: {}>'.format(self.name)

class Pallet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	bin_ = db.Column(db.String(60), db.ForeignKey('bin.name'))
	item_ = db.Column(db.String(10), db.ForeignKey('item.item_code'))
	lot_id = db.Column(db.String(60), db.ForeignKey('lot.name'))
	num_of_pieces = db.Column(db.Integer)
	created = db.Column(db.DateTime)

	def __repr__(self):
		return '<Pallet: {}>'.format(self.name)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item_code = db.Column(db.String(10), unique=True)
	description = db.Column(db.String(500))
	pallets = db.relationship('Pallet', backref='item', lazy='dynamic')

	def __repr__(self):
		return '<Item: {}>'.format(self.name)

class Lot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	created = db.Column(db.DateTime)
	
	pallets = db.relationship('Pallet', backref='lot', lazy='dynamic')
	
	def __repr__(self):
		return '<Lot: {}>'.format(self.name)



class Module(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	is_active = db.Column(db.Boolean, default=True)

	views = db.relationship('View', backref='module', lazy='dynamic')
	access = db.relationship('Access', back_populates='module')


	def __repr__(self):
		return '<Module: {}>'.format(self.name)


class View(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	is_active = db.Column(db.Boolean, default=True)
	module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

	sections = db.relationship('Section', backref='View', lazy='dynamic')
	access = db.relationship('Access', back_populates='views')


	def __repr__(self):
		return '<View: {}>'.format(self.name)


class Section(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	is_active = db.Column(db.Boolean, default=True)
	view_id = db.Column(db.Integer, db.ForeignKey('view.id'))
	view = db.relationship('View', back_populates='sections')
	
	# features = db.relationship('Feature', backref='Section', lazy='dynamic')
	access = db.relationship('Access', back_populates='section')

	
	def __repr__(self):
		return '<Section: {}>'.format(self.name)


class Feature(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	is_active = db.Column(db.Boolean, default=True)
	section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
	# section = db.relationship('Section', back_populates='features')

	# access = db.relationship('Access', back_populates='feature')

	def __repr__(self):
		return '<Feature: {}>'.format(self.name)

class User(UserMixin,db.Model):
	"""
	create user table
	"""

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	first_name = db.Column(db.String(60), index=True)
	last_name = db.Column(db.String(60), index=True)
	gender = db.Column(db.String(10), index=True)
	contact = db.Column(db.String(15), index=True)
	added_by = db.Column(db.Integer)
	registered = db.Column(db.DateTime)
	last_login = db.Column(db.DateTime)
	avatar = db.Column(db.String(100), index=True)
	
	department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	password_hash = db.Column(db.String(128))
	
	is_admin = db.Column(db.Boolean, default=False)
	is_active = db.Column(db.Boolean, default=True)
	is_logged_in = db.Column(db.Boolean, default=False)

	role = db.relationship('Role', back_populates='users')

	@property
	def password(self):
		"""
		Prevent password from being accessed
		"""
		raise AttributeError('password is not a readable attribute.')

	# return self._password
	@password.setter
	def password(self, value):
		"""
		Set password to a hashed password
		""" 
		self.password_hash = generate_password_hash(value)


	def verify_password(self, password):
		"""
		Check if hashed password matches actual password
		"""
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User: {}>'.format(self.username)


class Role(db.Model):
	"""
	Create a Role table
	"""
	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	
	users = db.relationship('User', back_populates='role')
	access = db.relationship('Access', back_populates='role')

	def __repr__(self):
		return '<Role: {}>'.format(self.name)


class Access(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	role = db.relationship('Role', back_populates='access')
	
	module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
	module = db.relationship('Module', back_populates='access')

	view_id = db.Column(db.Integer, db.ForeignKey('view.id'))
	views = db.relationship('View', back_populates='access')

	section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
	section = db.relationship('Section', back_populates='access')

	permission = db.Column(db.Integer)

	def __repr__(self):
		return '<Access: {}>'.format(self.id)

