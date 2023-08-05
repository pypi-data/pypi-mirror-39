#
# Copyright 2018 Russell Smiley
#
# This file is part of packager.
#
# packager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# packager is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with packager.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Test ``Package`` class.
"""

import unittest.mock

from distributionPackage.app import PackageOptions
from packageManifest import Manifest

from ..package import Package

# DO NOT DELETE. Used by unittest.mock.patch below.
import distributionPackage.package.package


class TestPackage( unittest.TestCase ) :

    def setUp( self ) :
        self.mockPackageOptions = unittest.mock.create_autospec( PackageOptions )
        self.mockPackageOptions.append = False
        self.mockPackageOptions.projectRoot = '.'


    def testTarPackage( self ) :
        """
        When tar package is selected, the tar package object build method is called.
        """
        self.mockPackageOptions.isTarFile = True
        self.mockPackageOptions.isZipFile = False

        with unittest.mock.patch( 'distributionPackage.package.package.TarPackage',
                                  autospec = True ) as mockTarPackage, \
                unittest.mock.patch( 'packageManifest.Manifest',
                                     autospec = True ) as mockManifest :
            packageUnderTest = Package( mockManifest, self.mockPackageOptions )
            packageUnderTest.build()

            mockManifest.apply.assert_called_once()

            mockTarPackageObject = mockTarPackage.return_value
            mockTarPackageObject.build.assert_called_once()


    def testZipPackage( self ) :
        """
        When zip package is selected, the zip package object build method is called.
        """
        self.mockPackageOptions.isTarFile = False
        self.mockPackageOptions.isZipFile = True

        with unittest.mock.patch( 'distributionPackage.package.package.ZipPackage',
                                  autospec = True ) as mockZipPackage, \
                unittest.mock.patch( 'packageManifest.Manifest',
                                     autospec = True ) as mockManifest :
            packageUnderTest = Package( mockManifest, self.mockPackageOptions )
            packageUnderTest.build()

            mockManifest.apply.assert_called_once()

            mockZipPackageObject = mockZipPackage.return_value
            mockZipPackageObject.build.assert_called_once()


    def testBothPackages( self ) :
        """
        User is able to package both tar and zip simultaneously.
        """
        self.mockPackageOptions.isTarFile = True
        self.mockPackageOptions.isZipFile = True

        with unittest.mock.patch( 'distributionPackage.package.package.TarPackage',
                                  autospec = True ) as mockTarPackage, \
                unittest.mock.patch( 'distributionPackage.package.package.ZipPackage',
                                     autospec = True ) as mockZipPackage, \
                unittest.mock.patch( 'packageManifest.Manifest',
                                     autospec = True ) as mockManifest :
            packageUnderTest = Package( mockManifest, self.mockPackageOptions )
            packageUnderTest.build()

            mockManifest.apply.assert_called_once()

            mockTarPackageObject = mockTarPackage.return_value
            mockTarPackageObject.build.assert_called_once()

            mockZipPackageObject = mockZipPackage.return_value
            mockZipPackageObject.build.assert_called_once()


if __name__ == '__main__' :
    unittest.main()
