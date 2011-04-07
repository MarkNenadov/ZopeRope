# zope2_fetch_objs.py - Zope External methods to extract Python Scripts and DTML Methods 
# from your Zope 2 Data.fs. They will extract the relevant objects off the root Zope 
# instance structure, including everything within Products and within ZClasses 
# that are embedded in products.
#
# - copy zope2_fetch_objs.py into Extensions folder
# - Create any of these external methods *in the root folder in your Zope instance 
#   management interface*:
#	- First one (id: extract_pyscripts, module name: zope2_fetch_objs, function name: 
#         extract_pyscripts) 
#	- Second one (id: extract_dtmlmethods, module name: zope2_fetch_objs, function: 
#	  extract_dtmlmethods)
#	- Third one (id: extract_tinytables, module name: zope2_fetch_objs, function: 
#	  extract_dtmlmethods)
# - Invoke from a url or from the Zope management interface: [ extract_pyscripts(full_path) 
#   or extract_dtmlmethods(full_path) ] 
#
#  by Mark J. Nenadov 2011
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

folders = []
products_or_zclasses = []

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

def extract(obj, ext, path):
	""" Extract a ZopeObjectWrapper and write it to the file system
	"""
	file_name = obj.get_id()

	if file_name != None:
		if (file_name.find("." + ext) == -1):
			file_name += "." + ext

	f = open(path + file_name, 'w')
	f.write(obj.get_content())
	f.close()

def extract_generic(self, obj_type, ext, path):
	""" Generically handle loading lists of folders and products/zclasses
	filter by meta_type and pass a ZopeObjectWrapper instance to the
	extraction function
	"""
	# iterate recursively to get folders
	folders = load_folders(self, first_run=1)

	# iterate recursively get products 
	products_or_zclasses = load_products_or_zclasses(self.Control_Panel.Products, first_run=1)

	for obj_container in folders + products_or_zclasses:
		for obj in obj_container.objectValues(obj_type):
			# not sure why this extra check is needed, 
			# somehow objectValues returns some unexpected objects
			if obj.meta_type == obj_type:
				extract(ZopeObjectWrapper(obj), ext, path)

def extract_pyscripts(self, path):
	""" Initiate extraction of Python Scripts to the file system
	"""

	extract_generic(self, "Script (Python)", 'py', path)

def extract_dtmlmethods(self, path):
	""" Initiate extraction of DTML Methods to the file system
	"""

	extract_generic(self, "DTML Method", 'dtml', path)

def extract_tinytables(self, path):
	""" Initiate extraction of TinyTables to the file system (in csv format)
	"""

	extract_generic(self, "TinyTable", "csv", path)
