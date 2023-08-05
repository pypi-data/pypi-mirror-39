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
Utility classes for unit tests.
"""

import os
import tempfile


class PackageTestData :
    """
    Manage mock file data for package tests.
    """

    subdirFoundCount = 0
    notFoundFileCount = 0

    addedFiles = set()


    def __init__( self ) :
        self.filesToPackage = {
            os.path.join( 'some', 'file' ),
            os.path.join( 'afile' ),
            os.path.join( 'some', 'subdir', 'file' ),
            os.path.join( 'some', 'subdir' ),
            os.path.join( 'notFound' ),
        }

        self.expectedPackagedFiles = {
            os.path.join( 'some', 'file' ),
            os.path.join( 'afile' ),
            os.path.join( 'some', 'subdir', 'file' ),
        }

        PackageTestData.subdirFoundCount = 0
        PackageTestData.notFoundFileCount = 0


    @staticmethod
    def mockOsIsfile( filename ) :
        if filename == os.path.join( 'some', 'subdir' ) :
            PackageTestData.subdirFoundCount += 1

            return False
        elif filename == 'notFound' :
            PackageTestData.notFoundFileCount += 1

            return False
        else :
            return True


class MockCompressedFile :

    def __init__( self ) :
        self.writtenFiles = set()


    def __enter__( self ) :
        return self


    def __exit__( self, exc_type, exc_val, exc_tb ) :
        pass


    def write( self, filename ) :
        """
        Mock ZipFile.write
        """
        self.writtenFiles.add( filename )


    def add( self, filename ) :
        """
        Mock tarfile.add
        """
        self.writtenFiles.add( filename )


class MockCompressedOpen( PackageTestData ) :

    def __init__( self ) :
        super().__init__()

        self.fileObject = MockCompressedFile()


    def __call__( self, *args, **kwargs ) :
        return self.fileObject


class AppendTestData( tempfile.TemporaryDirectory ) :
    """
    Manage temporary files for the package append test.
    """


    def __init__( self, *args, **kwargs ) :
        super().__init__( *args, **kwargs )

        self.tempDirectory = None

        self.file1 = 'file1'
        self.file2 = 'file2'


    def __enter__( self ) :
        self.tempDirectory = super().__enter__()

        with open( os.path.join( self.tempDirectory, self.file1 ), 'w' ) as f :
            f.write( 'Test file1' )

        with open( os.path.join( self.tempDirectory, self.file2 ), 'w' ) as f :
            f.write( 'Test file2' )

        return self


    def __exit__( self, exc_type, exc_val, exc_tb ) :
        super().__exit__( exc_type, exc_val, exc_tb )
