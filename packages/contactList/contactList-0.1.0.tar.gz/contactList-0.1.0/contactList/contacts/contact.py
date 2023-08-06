#
# Copyright 2018 Russell Smiley
#
# This file is part of contactList.
#
# contactList is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# contactList is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with contactList.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Core Contacts class implementation.
"""

import logging
import os
import yaml

from ..arguments import ContactsOptions

from .base import ContactData
from .cluster import ClusterOperation
from .email import EmailOperation
from .group import GroupOperation


log = logging.getLogger( __name__ )


class Contacts :
    """
    Management of contact groups and clusters.
    """

    __DEFAULT_FILE = 'contacts.yml'
    __YAML_KEYS = {
        'cluster' : 'clusters',
        'group' : 'groups',
    }


    def __init__( self ) :
        self.data = ContactData()
        self.subcommands = {
            'cluster' : ClusterOperation(),
            'email' : EmailOperation(),
            'group' : GroupOperation(),
        }


    def applyAction( self, contactsOptions: ContactsOptions ) :
        actionName = contactsOptions.activeSubcommand
        subcommand = self.subcommands[ actionName ]

        subcommand.applyOperation( self.data, contactsOptions )


    def to_yamlFile( self,
                     filename = None,
                     fileObject = None ) :
        """
        Write the contacts data to a file in YAML format. Either a filename or a file object must be specified,
        or accept the default filename.

        :param filename: (optional)
        :param fileObject: (optional)
        """

        assert not ((filename is not None) and (fileObject is not None))

        if fileObject is None :
            # Explicitly open a file.
            if filename is None :
                # Use default file name.
                filePath = Contacts.__DEFAULT_FILE
            else :
                filePath = filename

            with open( filePath, 'w' ) as fileObject :
                self.__exportData( fileObject )
        else :
            # Use the user defined file object.
            self.__exportData( fileObject )


    def __exportData( self, fileObject ) :
        exportYamlData = {
            self.__YAML_KEYS[ 'cluster' ] : self.data.clusters,
            self.__YAML_KEYS[ 'group' ] : self.data.groups,
        }

        yaml.dump( exportYamlData, fileObject )


    def __parseGroups( self, yamlData ) :
        if self.__YAML_KEYS[ 'group' ] in yamlData :
            assert isinstance( yamlData[ self.__YAML_KEYS[ 'group' ] ], dict )

            self.data.groups = yamlData[ self.__YAML_KEYS[ 'group' ] ]


    def __parseClusters( self, yamlData ) :
        if self.__YAML_KEYS[ 'cluster' ] in yamlData :
            assert isinstance( yamlData[ self.__YAML_KEYS[ 'cluster' ] ], dict )

            self.data.clusters = yamlData[ self.__YAML_KEYS[ 'cluster' ] ]


    @classmethod
    def from_yamlData( cls, yamlData ) :
        """
        Recover contacts data from YAML data structure.

        :param yamlData: YAML data loaded using ``yaml.load`` or ``yaml.safeload``.

        :return: Constructed ``Contacts`` object.
        """
        contactObject = cls()

        if yamlData is not None :
            contactObject.__parseGroups( yamlData )
            contactObject.__parseClusters( yamlData )

        return contactObject


    @classmethod
    def from_yamlFile( cls,
                       filename: str = None,
                       fileObject = None ) :
        """
        Load contacts data from a YAML file or file object.

        :param filename: Name of YAML file (optional)
        :param fileObject: File object (optional)

        :return: Constructed ``Contacts`` object.
        """


        def loadData() :
            yamlData = yaml.safe_load( fileObject )

            thisObject = cls.from_yamlData( yamlData )

            return thisObject


        assert not ((filename is not None) and (fileObject is not None))

        if fileObject is None :
            # Explicitly open a file.
            if filename is None :
                # Use default file name.
                filePath = Contacts.__DEFAULT_FILE
            else :
                filePath = filename

            if os.path.isfile( filePath ) :
                with open( filePath, 'r' ) as fileObject :
                    contactsObject = loadData()
            else :
                raise FileNotFoundError( 'File does not exist, {0}'.format( filePath ) )
        else :
            # Use the user defined file object.
            contactsObject = loadData()

        contactsObject.data.validate()

        return contactsObject
