# zope2_pyscript_fetch.py
#
# Add this as an External Method to Zope to extract Python Scripts from
# your Zope 2 installation
#
# - modify the save_path variable in zope2_pyscript_fetch.py to a path suitable for you
# - copy zope2_pyscript_fetch.py into Extensions folder
# - Create an external method (id: whatever name you want, module name: zope2_pyscript_fetch, function name: extract_python_scripts
# - Invoke the external method you created (either through a url or through a dtml method with dtml-call) with no arguments
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
save_path = 'e://tmp/'

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

def save_script(script):
	file_name = script.id

	if (file_name.find(".py") == -1):
		file_name += ".py"
	
	f = open(save_path + file_name, 'w')
	f.write(script.document_src())
	f.close()

def extract_python_scripts(self):
	folders = load_folders(self, first_run=1)
	for folder in folders:
		for script in folder.objectValues("Script (Python)"):
			save_script(script)
