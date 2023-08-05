#
# Copyright 2018 Russell Smiley
#
# This file is part of distributionPackage.
#
# distributionPackage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# distributionPackage is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with distributionPackage.  If not, see <http://www.gnu.org/licenses/>.
#

"""
``ZipPackage`` implementation.
"""

import os
import logging
import zipfile

from .base import PackageBase
from .directory import ChangeDirectory
from .interface import PackageInterface


log = logging.getLogger( __name__ )


class ZipPackage( PackageInterface, PackageBase ) :
    """
    Coordinate building a zip package from specified files.
    """

    def __init__( self, fileName, projectRoot, append ) :
        super().__init__( fileName, projectRoot, append )


    def build( self, filesToPackage ) :
        if self.append and os.path.isfile( self.fileName ) :
            self.__openForAppend( filesToPackage )
        else :
            self.__openForWrite( filesToPackage )


    def __openForAppend( self, filesToPackage ) :
        log.info( 'Appending to existing file, {0}'.format( self.fileName ) )
        with  zipfile.ZipFile( self.fileName,
                               mode = 'a' ) as thisZipfile :
            self.__doBuild( filesToPackage, thisZipfile )


    def __openForWrite( self, filesToPackage ) :
        with zipfile.ZipFile( self.fileName,
                              mode = 'w' ) as thisZipfile :
            self.__doBuild( filesToPackage, thisZipfile )


    def __doBuild( self, filesToPackage, thisZipfile ) :
        with ChangeDirectory( self.projectRoot ) :
            for thisFile in filesToPackage :
                if os.path.isfile( thisFile ) :
                    thisZipfile.write( thisFile )
                elif not os.path.exists( thisFile ) :
                    realFileName = os.path.realpath( os.path.abspath( os.path.join( self.projectRoot, thisFile ) ) )

                    log.warning( 'File to package does not exist, {0}'.format( realFileName ) )
