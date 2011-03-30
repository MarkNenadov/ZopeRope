# zope2_propertysheet_to_sql.py
#
# A Zope PythonScript that takes all property sheets for a ZClass instance and outputs the SQL schema for a singular table representing all the properties as well as
# an SQL insert representing that object's particular property values.
#
# Three notes you should read before attempting to use this:
#
# 1. This is not a standalone Python script. Do not attempt to run it with your Python interpreter, it will not run like that without adjustments. It's meant to be
# created as a "Script (Python)" in Zope 2. Go into the management interface, find the Zclass that you want to use it in, add a "Script (Python)" to your ZClass, 
# paste the code into it, save it, and execute it.
#
# 2. This is intended to give you a bit of a head start in representing your ZClasses as SQL tables as you migrate away from Zope 2. It should be a time saver if you
# are migrating away from Zope 2, have many ZClasses, have used ZODB primarily, and need to design an SQL schema. Please note that you will 
# most likely have to tweak the resulting tables and add any relations you want. While this script should give you a working SQL table and record, the SQL it outputs is
# obviously automated and supports a limited number of SQL field types. 
#
# 3. As of now, it only supports VARCHAR, INT, and FLOAT. Strings, no matter how long they are, will be stuffed into a VARCHAR(255). If it is neither a string, integer,
# or float, the script will attempt to put it into a VARCHAR(255).  I've tested this on 3 large production ZClasses with a variety of fields, and in each case it produce
# valid SQL statements to build the table and insert the data
#
# License:
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

FLOAT_TYPE = 1.0
INT_TYPE = 1
STRING_TYPE = " "

table_properties = {}

for item in context.propertysheets.items():
    for property_sheet in item:
           try:
               for property in property_sheet.propertyItems():
                   if property[0] not in ['getcontentlength', 'getcontenttype', 'creationdate', 'getlastmodified', 'supportedlock', 'resourcetype', 'lockdiscovery']:
                           table_properties[property[0]] = property[1]
           except AttributeError:
               pass



sql_str = "CREATE TABLE propertysheet ("
count = 1
separator = ", "

for property in table_properties.keys():
    if count == len(table_properties.keys()): 
        separator = ""
    if same_type(table_properties[property], STRING_TYPE):
        sql_str += property + " VARCHAR(255)" + separator
    elif same_type(table_properties[property], INT_TYPE):
        sql_str += property + " INT" + separator
    elif same_type(table_properties[property], FLOAT_TYPE):
        sql_str += property + " FLOAT" + separator
    else:
        sql_str += property + " VARCHAR(255)" + separator
    count += 1

sql_str += ");"

sql_str += "\n\nINSERT INTO propertysheet ("
count = 1
separator = ", "

for property in table_properties.keys():
    if count == len(table_properties.keys()):
        separator = ""
    sql_str += property + separator
    count += 1

sql_str += ") VALUES ("
separator = ", "
count = 1

for property in table_properties.keys():
    if count == len(table_properties.keys()): 
        separator = ""
    if same_type(table_properties[property], STRING_TYPE):
        sql_str +=  " '" + table_properties[property] + "'" + separator
    elif same_type(table_properties[property], INT_TYPE):
        sql_str +=  str(table_properties[property]) + separator
    elif same_type(table_properties[property], FLOAT_TYPE):
        sql_str +=  str(table_properties[property]) + separator
    else:
        sql_str +=  " '" + str(table_properties[property]) + "'" + separator
    count += 1


sql_str += ");"

return sql_str

