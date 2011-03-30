-- ZopeRope - Various tools for migrating away from Zope (particularly v2) --


Created by Mark J. Nenadov 2011

License:

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

--


Tool # 1 - zope2_pyscript_fetch.py

Searches through a Zope installation (excluding Zope Products) and extracts Python Script into .py files.

You will need to add this script as an External Method to Zope to extract Python Scripts from your Zope 2 installation.

Instructions:
1. modify the save_path variable in zope2_pyscript_fetch.py to a path suitable for you
2. copy zope2_pyscript_fetch.py into Extensions folder
3. Create an external method (id: whatever name you want, module name: zope2_pyscript_fetch, function name: extract_python_scripts
4. Invoke the external method you created (either through a url or through a dtml method with dtml-call) with no arguments

Limitation: It iterates through all folders in the instance from the root folder onwards, but doesn't look at Products.


--

Tool #2 - zope2_propertysheet_to_sql.py

 A Zope PythonScript that takes all property sheets for a ZClass instance and outputs the SQL schema for a singular table representing all the properties as well as
 an SQL insert representing that object's particular property values.

 Three notes you should read before attempting to use this:

 1. This is not a standalone Python script. Do not attempt to run it with your Python interpreter, it will not run like that without adjustments. It's meant to be
 created as a "Script (Python)" in Zope 2. Go into the management interface, find the Zclass that you want to use it in, add a "Script (Python)" to your ZClass, 
 paste the code into it, save it, and execute it.

 2. This is intended to give you a bit of a head start in representing your ZClasses as SQL tables as you migrate away from Zope 2. It should be a time saver if you
 are migrating away from Zope 2, have many ZClasses, have used ZODB primarily, and need to design an SQL schema. Please note that you will 
 most likely have to tweak the resulting tables and add any relations you want. While this script should give you a working SQL table and record, the SQL it outputs is
 obviously automated and supports a limited number of SQL field types. 

 3. As of now, it only supports VARCHAR, INT, and FLOAT. Strings, no matter how long they are, will be stuffed into a VARCHAR(255). If it is neither a string, integer,
 or float, the script will attempt to put it into a VARCHAR(255).  I've tested this on 3 large production ZClasses with a variety of fields, and in each case it produce
 valid SQL statements to build the table and insert the data