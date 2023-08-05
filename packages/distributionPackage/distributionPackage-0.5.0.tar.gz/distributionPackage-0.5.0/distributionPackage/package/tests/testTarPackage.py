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
Test ``TarPackage`` class.
"""

import os
import unittest.mock

from .utility import \
    AppendTestData, \
    MockCompressedOpen, \
    PackageTestData

from ..tarPackage import \
    TarPackage, \
    tarfile

import distributionPackage.package.tarPackage


class TestTarPackage( unittest.TestCase ) :
    """
    Test ``TarPackage`` class.
    """


    def setUp( self ) :
        self.data = PackageTestData()


    def testAppendDisabledCreatesNonexistentFile( self ) :
        appendMode = False
        mockTarFile = unittest.mock.create_autospec( tarfile.TarFile )

        with unittest.mock.patch( 'tarfile.open',
                                  return_value = mockTarFile ) as mockTarOpen :
            with unittest.mock.patch(
                    'distributionPackage.package.tarPackage.TarPackage._TarPackage__doBuild' ) as mock_doBuild :
                packageUnderTest = TarPackage( self.id(), '.', appendMode )

                packageUnderTest.build( self.data.filesToPackage )

        mockTarOpen.assert_called_with( name = self.id(),
                                        mode = 'w:gz' )


    def testSubdirIsDiscovered( self ) :
        expectedSubdirFoundCount = 1

        mockTarFile = unittest.mock.create_autospec( tarfile.TarFile )

        with unittest.mock.patch( 'os.path.isfile',
                                  side_effect = PackageTestData.mockOsIsfile ), \
             unittest.mock.patch( 'tarfile.open',
                                  return_value = mockTarFile ) :
            packageUnderTest = TarPackage( self.id(), '.', False )

            packageUnderTest.build( self.data.filesToPackage )

        self.assertEqual( expectedSubdirFoundCount, self.data.subdirFoundCount )


    def testAddedFiles( self ) :
        with unittest.mock.patch( 'os.path.isfile',
                                  side_effect = PackageTestData.mockOsIsfile ), \
             unittest.mock.patch( 'tarfile.open',
                                  new_callable = MockCompressedOpen ) as mock_zipfile, \
                unittest.mock.patch( 'distributionPackage.package.tarPackage.ChangeDirectory',
                                     autospec = True ) :
            packageUnderTest = TarPackage( self.id(), '.', False )
            packageUnderTest.build( self.data.filesToPackage )

            self.assertEqual( self.data.expectedPackagedFiles, mock_zipfile.fileObject.writtenFiles )


class TestTarPackageAppendMode( unittest.TestCase ) :
    """
    Test ``TarPackage`` append mode.
    """


    def setUp( self ) :
        self.data = PackageTestData()


    def testAppendCreatesNonexistentFile( self ) :
        """
        Append mode on a non-existent file silently creates the file.
        :return:
        """
        appendMode = True

        with unittest.mock.patch( 'os.path.isfile',
                                  return_value = False ) as mockOsIsfile :
            with unittest.mock.patch(
                    'distributionPackage.package.tarPackage.TarPackage._TarPackage__openForWrite' ) as \
                    mock_write :
                packageUnderTest = TarPackage( self.id(), '.', appendMode )
                packageUnderTest.build( self.data.filesToPackage )

                # If "openForWrite" is called then the file is created (or overwritten, but in this case the file
                # doesn't exist).
                mock_write.assert_called_once_with( self.data.filesToPackage )


    def testAppendToFile( self ) :
        appendMode = True
        mockTarFile = unittest.mock.create_autospec( tarfile.TarFile )

        with unittest.mock.patch( 'tarfile.open',
                                  return_value = mockTarFile ) as mockTarOpen, \
                unittest.mock.patch( 'os.path.isfile',
                                     return_value = False ) as mockOsIsfile, \
                unittest.mock.patch(
                    'distributionPackage.package.tarPackage.TarPackage._TarPackage__doBuild' ) as mock_doBuild :
            packageUnderTest = TarPackage( self.id(), '.', appendMode )

            packageUnderTest.build( self.data.filesToPackage )

            mockTarOpen.assert_called_with( name = self.id(),
                                            mode = 'w:gz' )


class TestTarPackageAppend( unittest.TestCase ) :
    """
    Test an actual append operation.
    """


    def testAppendFile( self ) :
        with AppendTestData() as appendData :
            packageFile = os.path.join( appendData.tempDirectory, self.id() )

            packageUnderTest = TarPackage( packageFile, appendData.tempDirectory, False )
            packageUnderTest.build( { 'file1' } )

            self.assertTrue( os.path.exists( packageFile ) )

            packageUnderTest.append = True
            packageUnderTest.build( { 'file2' } )

            with tarfile.open( packageFile, 'r:gz' ) as extractTar :
                info = set( extractTar.getnames() )

            self.assertEqual( { 'file1', 'file2' }, info )


if __name__ == '__main__' :
    unittest.main()
