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