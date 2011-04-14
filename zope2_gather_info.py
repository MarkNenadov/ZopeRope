"""zope2_gather_info

An external method for the purposes of gather information about a Zope 2
instance that will be helpful in assessing what migration away from it will
look like. 


A Zope External method to gather information about a Zope 2 instance
and return it in the form of a dictionary. It should be helpful in
gauging what might be involved in migrating away from that instance
to a different platform without having to get into the nitty-gritty.

Steps:
 - Copy zoperope_support lib into somewhere in your Zope instances Python 
   module include path (ie. bin/lib/ within your Zope instance folder)
 - Copy zope2_gather_info.py into Extensions folder
 - Create an external method *in the root folder in your Zope 
   instance management interface*:
	- (id: get_instance_info, module name: zope2_gather_info, 
	  function name: get_instance_info) 
 - Invoke it zope2_gather_info()

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

from zoperope_support_lib import load_folders
from zoperope_support_lib import load_products_or_zclasses
from zoperope_support_lib import ZopeObjectWrapper
from zoperope_support_lib import get_root_folder

def get_instance_info(self):
    """ Generate a dictionary about various details from a Zope instance
    relevant to assessing what migration will look like.
    """

    instance_info = {}
    instance_info['Script (Python)'] = {}
    instance_info['Script (Python)']['num'] = 0
    instance_info['Script (Python)']['lines'] = 0
    instance_info['DTML Method'] = {}
    instance_info['DTML Method']['num'] = 0
    instance_info['DTML Method']['lines'] = 0
    instance_info['TinyTable'] = {}
    instance_info['TinyTable']['num'] = 0
    instance_info['TinyTable']['lines'] = 0

    cp_products = get_root_folder().Control_Panel.Products

    folders = load_folders(get_root_folder(), [])
    products_or_zclasses = load_products_or_zclasses(cp_products, [])

    for meta_type in instance_info.keys():
        for obj_container in folders + products_or_zclasses:
            for working_object in obj_container.objectValues(meta_type):
                obj = ZopeObjectWrapper(working_object)
                obj_content = obj.get_content()
           
                if obj_content != None:	    
                    instance_info[meta_type]['num'] += 1
                    if meta_type == "TinyTable":
                        num_lines = len(obj_content)
                    else:
                        num_lines = len(obj_content.split('\n'))

                    instance_info[meta_type]['lines'] += num_lines


    return instance_info
