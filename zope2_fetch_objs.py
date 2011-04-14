""" zope2_fetch_objs.py 

Zope External methods to extract Python Scripts and DTML Methods 
from your Zope 2 Data.fs. They will extract the relevant objects off 
the root Zope instance structure, including everything within Products 
and within ZClasses that are embedded in products.

Steps:
 - Copy zoperope_support lib into somewhere in your Zope instances Python 
   module include path (ie. bin/lib/ within your Zope instance folder)
 - Copy zope2_fetch_objs.py into Extensions folder
 - Create any of these external methods *in the root folder in your Zope 
   instance management interface*:
	- First one (id: extract_pyscripts, module name: zope2_fetch_objs, 
	  function name: extract_pyscripts) 
	- Second one (id: extract_dtmlmethods, module name: zope2_fetch_objs, 
	  function: extract_dtmlmethods)
	- Third one (id: extract_tinytables, module name: zope2_fetch_objs, function: 
	  extract_dtmlmethods)
 - Invoke from a url or from the Zope management interface: 
 	[ extract_pyscripts(full_path) or extract_dtmlmethods(full_path)
	  or extract_tinytables(full_path) ]

(Tested with pylint (10/10 score with default config))

by Mark J. Nenadov 2011

License:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from zoperope_support_lib import ZopeObjectWrapper
from zoperope_support_lib import load_folders
from zoperope_support_lib import load_products_or_zclasses
from zoperope_support_lib import get_root_folder

def extract(obj, ext, path):
    """ Extract a ZopeObjectWrapper and write it to the file system
    """
    file_name = obj.get_id()

    if file_name != None:
        if (file_name.find("." + ext) == -1):
            file_name += "." + ext

    out_file = open(path + file_name, 'w')
    out_file.write(obj.get_content())
    out_file.close()

def extract_generic(self, obj_type, ext, path):
    """ Generically handle loading lists of folders and products/zclasses
    filter by meta_type and pass a ZopeObjectWrapper instance to the
    extraction function
    """
    cp_products = get_root_folder().Control_Panel.Products

    # iterate recursively to get folders
    folders = load_folders(self, [])

    # iterate recursively get products 
    products_or_zclasses = load_products_or_zclasses(cp_products, [])

    for obj_container in folders + products_or_zclasses:
	    
        for obj in obj_container.objectValues(obj_type):
	    # not sure why this extra check is needed, 
            # somehow objectValues returns some unexpected objects

            if obj.meta_type == obj_type:
                extract(ZopeObjectWrapper(obj), ext, path)

def extract_pyscripts(self, path):
    """ Initiate extraction of Python Scripts to the file system
    """

    extract_generic(get_root_folder(), "Script (Python)", 'py', path)

def extract_dtmlmethods(self, path):
    """ Initiate extraction of DTML Methods to the file system
    """

    extract_generic(self, "DTML Method", 'dtml', path)

def extract_tinytables(self, path):
    """ Initiate extraction of TinyTables to the file system (in csv format)
    """
	
    extract_generic(get_root_folder(), "TinyTable", "csv", path)
