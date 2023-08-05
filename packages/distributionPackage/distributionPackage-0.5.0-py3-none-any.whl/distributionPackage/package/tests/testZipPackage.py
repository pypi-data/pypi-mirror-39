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
Test ``ZipPackage`` class.
"""

import os
import unittest.mock

from .utility import \
    AppendTestData, \
    MockCompressedOpen, \
    PackageTestData

from ..zipPackage import \
    ZipPackage, \
    zipfile

import distributionPackage.package.zipPackage


class TestZipPackage( unittest.TestCase ) :
    """
    Test ``ZipPackage`` class.
    """


    def setUp( self ) :
        self.data = PackageTestData()


    def testAppendDisabledCreatesNonexistentFile( self ) :
        appendMode = False

        with unittest.mock.patch(
                'distributionPackage.package.zipPackage.ZipPackage._ZipPackage__doBuild' ) as mock_doBuild, \
                unittest.mock.patch(
                    'distributionPackage.package.zipPackage.zipfile.ZipFile' ) as mockZipFile :
            packageUnderTest = ZipPackage( self.id(), '.', appendMode )

            packageUnderTest.build( self.data.filesToPackage )

        mockZipFile.assert_called_with( self.id(),
                                        mode = 'w' )


    def testNonExistentFileIsDiscovered( self ) :
        expectedNotFoundCount = 1

        with unittest.mock.patch( 'os.path.isfile',
                                  side_effect = PackageTestData.mockOsIsfile ), \
             unittest.mock.patch( 'distributionPackage.package.zipPackage.zipfile.ZipFile' ) :
            packageUnderTest = ZipPackage( self.id(), '.', False )

            packageUnderTest.build( self.data.filesToPackage )

        self.assertEqual( expectedNotFoundCount, self.data.notFoundFileCount )


    def testSubdirIsDiscovered( self ) :
        expectedSubdirFoundCount = 1

        with unittest.mock.patch( 'os.path.isfile',
                                  side_effect = PackageTestData.mockOsIsfile ), \
             unittest.mock.patch( 'distributionPackage.package.zipPackage.zipfile.ZipFile' ) :
            packageUnderTest = ZipPackage( self.id(), '.', False )

            packageUnderTest.build( self.data.filesToPackage )

        self.assertEqual( expectedSubdirFoundCount, self.data.subdirFoundCount )


    def testAddedFiles( self ) :
        with unittest.mock.patch( 'os.path.isfile',
                                  side_effect = PackageTestData.mockOsIsfile ), \
             unittest.mock.patch( 'distributionPackage.package.zipPackage.zipfile.ZipFile',
                                  new_callable = MockCompressedOpen ) as mock_zipfile, \
                unittest.mock.patch( 'distributionPackage.package.zipPackage.ChangeDirectory',
                                     autospec = True ) :
            packageUnderTest = ZipPackage( self.id(), '.', False )
            packageUnderTest.build( self.data.filesToPackage )

            self.assertEqual( self.data.expectedPackagedFiles, mock_zipfile.fileObject.writtenFiles )


class TestZipPackageAppendMode( unittest.TestCase ) :
    """
    Test ``ZipPackage`` append mode.
    """


    def setUp( self ) :
        self.data = PackageTestData()


    def testAppendCreatesNonexistentFile( self ) :
        appendMode = True

        with unittest.mock.patch( 'os.path.isfile', return_value = True ) as mockOsIsfile :
            with unittest.mock.patch(
                    'distributionPackage.package.tarPackage.TarPackage._TarPackage__doBuild' ) as mock_doBuild :
                with unittest.mock.patch(
                        'distributionPackage.package.zipPackage.zipfile.ZipFile' ) as mockZipFile :
                    packageUnderTest = ZipPackage( self.id(), '.', appendMode )

                    packageUnderTest.build( self.data.filesToPackage )

                    mockZipFile.assert_called_with( self.id(),
                                                    mode = 'a' )


    def testAppendToFile( self ) :
        appendMode = True

        with unittest.mock.patch( 'os.path.isfile', return_value = False ) as mockOsIsfile :
            with unittest.mock.patch( 'os.path.exists', return_value = False ) as mockOsExists :
                with unittest.mock.patch(
                        'distributionPackage.package.zipPackage.ZipPackage._ZipPackage__doBuild' ) as mock_doBuild :
                    with unittest.mock.patch(
                            'distributionPackage.package.zipPackage.zipfile.ZipFile' ) as mockZipFile :
                        packageUnderTest = ZipPackage( self.id(), '.', appendMode )

                        packageUnderTest.build( self.data.filesToPackage )

                        mockZipFile.assert_called_with( self.id(),
                                                        mode = 'w' )


class TestZipPackageAppend( unittest.TestCase ) :
    """
    Test an actual append operation.
    """


    def testAppendFile( self ) :
        with AppendTestData() as appendData :
            packageFile = os.path.join( appendData.tempDirectory, self.id() )

            packageUnderTest = ZipPackage( packageFile, appendData.tempDirectory, False )
            packageUnderTest.build( { 'file1' } )

            self.assertTrue( os.path.exists( packageFile ) )

            packageUnderTest.append = True
            packageUnderTest.build( { 'file2' } )

            with zipfile.ZipFile( packageFile ) as extractZip :
                info = extractZip.infolist()

            actualItems = { x.filename for x in info }
            self.assertEqual( { 'file1', 'file2' }, actualItems )


if __name__ == '__main__' :
    unittest.main()
