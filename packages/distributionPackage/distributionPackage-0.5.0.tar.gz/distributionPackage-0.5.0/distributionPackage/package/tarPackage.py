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
``TarPackage`` implementation.
"""

import gzip
import io
import logging
import os
import tarfile

from .base import PackageBase
from .directory import ChangeDirectory
from .interface import PackageInterface


log = logging.getLogger( __name__ )


class TarPackage( PackageInterface, PackageBase ) :
    """
    Coordinate building a tar package from specified files.
    """


    def __init__( self, fileName, projectRoot, append ) :
        super().__init__( fileName, projectRoot, append )

        self.gzipFile = None
        self.tarFile = None


    def build( self, filesToPackage ) :
        """
        Build the tar package using the specified files.

        :param filesToPackage:
        """
        if self.append and os.path.isfile( self.fileName ) :
            self.__openForAppend( filesToPackage )
        else :
            self.__openForWrite( filesToPackage )


    def __openForAppend( self, filesToPackage ) :
        log.info( 'Appending to existing file, {0}'.format( self.fileName ) )

        buffer = io.BytesIO()
        with gzip.open( self.fileName ) as thisGzip :
            buffer.write( thisGzip.read() )

        buffer.seek( 0 )

        with tarfile.open( fileobj = buffer,
                           mode = 'a' ) as thisFile :
            self.__doBuild( filesToPackage, thisFile )

        buffer.seek( 0 )
        with gzip.open( self.fileName, 'wb' ) as thisGzip :
            thisGzip.write( buffer.read() )


    def __openForWrite( self, filesToPackage ) :
        log.info( 'Opening or creating file for write, {0}'.format( self.fileName ) )
        with tarfile.open( name = self.fileName,
                           mode = 'w:gz' ) as thisFile :
            self.__doBuild( filesToPackage, thisFile )


    def __doBuild( self, filesToPackage, thisTarfile ) :
        """
        Temporarily change into the project directory and add the specified files to the package.

        :param filesToPackage:
        :return:
        """
        with ChangeDirectory( self.projectRoot ) :
            for thisFile in filesToPackage :
                if os.path.isfile( thisFile ) :
                    thisTarfile.add( thisFile )
                elif not os.path.exists( thisFile ) :
                    realFileName = os.path.realpath( os.path.abspath( os.path.join( self.projectRoot, thisFile ) ) )

                    log.warning( 'File to package does not exist, {0}'.format( realFileName ) )
