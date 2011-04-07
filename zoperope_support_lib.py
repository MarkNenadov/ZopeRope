class ZopeObjectWrapper:
	id = None
	content = None

	def __init__(self, obj):
		""" Constructor, handle getting object id and content,
		based on meta_type
		"""

		if (obj.meta_type == "DTML Method"):
			self.id = obj.id()
			self.content = obj.raw
		elif (obj.meta_type == "Script (Python)"):
			self.id = obj.id
			self.content = obj.document_src()
		elif (obj.meta_type == "TinyTable"):
			self.id = obj.id

			"""I don't use a CSV module here because
			there isn't a built-in one until Python 2.3"""

			s = obj.cols_text().replace(' ', ',').replace('"', '') + "\n"
			for line in obj.data_text():
				s += line
			self.content = s

	def get_id(self):
		return self.id

	def get_content(self):
		return self.content

def load_folders(container, first_run=0):
	""" Recursively build a list of folders in the Zope instance 
	"""
	global folders

	if first_run:
		folders = []

	contained_folders = container.objectValues('Folder')

	for folder in contained_folders:
		if len(contained_folders) != 0: 
			folders.append(folder)
			load_folders(folder)

	return folders

def load_products_or_zclasses(container, first_run=0, ):
	""" Recursively build a list of Products and ZClasses in the
	Products Management section
	"""
	global products_or_zclasses

	if first_run:
		products_or_zclasses = []
		contained_containers = container.objectValues('Product')
	else:
		contained_containers = container.objectValues('Z Class')

	for product_or_zclass in contained_containers:
		if len(contained_containers) != 0:
			products_or_zclasses.append(product_or_zclass)
			load_products_or_zclasses(product_or_zclass)

	return products_or_zclasses

