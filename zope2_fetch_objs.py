# zope2_fetch_objs.py - Zope External methods to extract Python Scripts and DTML Methods 
# from your Zope 2 Data.fs over to your filesystem
#
# - copy zope2_fetch_objs.py into Extensions folder
# - Create any of these external methods:
#	- First one (id: extract_pyscripts, module name: zope2_fetch_objs, function name: extract_pyscripts) 
#	- Second one (id: extract_dtmlmethods, module name: zope2_fetch_objs, function: extract_dtmlmethods)
# - Invoke: [ extract_pyscripts(full_path) or extract_dtmlmethods(full_path) ] from a url or from the Zope management interface
#
# Limitations:
#
# - Doesn't look in Zope Products
#
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

def load_folders(container, first_run=0):
	global folders

	if first_run:
		folders = []

	contained_folders = container.objectValues('Folder')

	for folder in contained_folders:
		if len(contained_folders) != 0: 
			folders.append(folder)
			load_folders(folder)

	return folders

def extract(obj, ext, path):
	if ext == 'dtml':
		file_name = obj.id()
	elif ext == 'py':
		file_name = obj.id

	if (file_name.find("." + ext) == -1):
		file_name += "." + ext
	
	f = open(path + file_name, 'w')

	if ext == 'dtml':
		src = obj.raw
	elif ext == 'py':
		src = obj.document_src()

	f.write(src)
	f.close()

def extract_generic(self, obj_type, ext, path):
	folders = load_folders(self, first_run=1)
	for folder in folders:
		for obj in folder.objectValues(obj_type):
			extract(obj, ext, path)

def extract_pyscripts(self, path):
	extract_generic(self, "Script (Python)", 'py', path)

def extract_dtmlmethods(self, path):
	extract_generic(self, "DTML Method", 'dtml', path)

