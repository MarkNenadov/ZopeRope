""" support Classes and functions for ZopeRope

(Tested with pylint (10/10 score with default config))

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

class ZopeObjectWrapper:
    """Attempts to provide a consistent interface to access the id and content
    of Zope objects
    """
    o_id = None
    o_content = None
    o_meta_type = None

    def __init__(self, obj):
        """ Constructor, handle getting object id and content,
        based on meta_type
        """
        
        self.o_meta_type = obj.meta_type

        if (obj.meta_type == "DTML Method"):
            self.o_id = obj.id()
            self.o_content = obj.raw
        elif (obj.meta_type == "Script (Python)"):
            self.o_id = obj.id
            self.o_content = obj.document_src()
        elif (obj.meta_type == "TinyTable"):
            self.o_id = obj.id
            self.o_content = obj.cols_text()
               
	    # not using csv module, because Python < 2.3 doesn't include one 

            tmp_str = self.o_content.replace(' ', ',').replace('"', '') + "\n"
                
            for line in obj.data_text():
                tmp_str += line
            self.content = tmp_str

    def get_id(self):
        """ Get id 
        """
        return self.o_id

    def get_content(self):
        """ Get content
        """
        return self.o_content
        
    def get_meta_type(self):
        """ Get meta type
        """
        return self.o_meta_type

def load_folders(container, folders):
    """ Recursively build a list of folders in the Zope instance 
    """
    
    contained_folders = container.objectValues('Folder')

    for folder in contained_folders:
        if len(contained_folders) != 0: 
            folders.append(folder)
            load_folders(folder, folders)

    return folders

def load_products_or_zclasses(container, products_or_zclasses):
    """ Recursively build a list of Products and ZClasses in the
    Products Management section
    """

    if len(products_or_zclasses) == 0:
        contained_containers = container.objectValues('Product')
    else:
        contained_containers = container.objectValues('Z Class')

    for product_or_zclass in contained_containers:
        if len(contained_containers) != 0:
            products_or_zclasses.append(product_or_zclass)
            load_products_or_zclasses(product_or_zclass, products_or_zclasses)

    return products_or_zclasses

def get_root_folder(request):
    return request.PARENTS[-1]
