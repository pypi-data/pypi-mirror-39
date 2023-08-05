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
Test user specified packaging options.
"""

import os
import unittest

from ..options import PackageOptions


class TestPackageOptions( unittest.TestCase ) :

    def setUp( self ) :
        self.optionsUnderTest = PackageOptions()


    def testDefaults( self ) :
        self.assertIsNone( self.optionsUnderTest.append )
        self.assertIsNone( self.optionsUnderTest.manifest )
        self.assertIsNone( self.optionsUnderTest.output )
        self.assertIsNone( self.optionsUnderTest.package )
        self.assertIsNone( self.optionsUnderTest.projectRoot )
        self.assertIsNone( self.optionsUnderTest.isTarFile )
        self.assertIsNone( self.optionsUnderTest.isZipFile )


    def testManifestPath( self ) :
        self.optionsUnderTest.manifest = 'some/path'

        self.assertEqual( self.optionsUnderTest.manifest, self.optionsUnderTest.manifestPath )


    def testTarPackagePathEnabled( self ) :
        self.optionsUnderTest.isTarFile = True
        self.optionsUnderTest.output = 'some/path'
        self.optionsUnderTest.package = 'package-name'

        expectedPath = os.path.join( self.optionsUnderTest.output, '{0}.tar.gz'.format( self.optionsUnderTest.package
                                                                                        ) )

        self.assertEqual( expectedPath, self.optionsUnderTest.tarPackagePath )


    def testTarPackagePathDisabled( self ) :
        self.optionsUnderTest.isTarFile = False

        self.assertIsNone( self.optionsUnderTest.tarPackagePath )


    def testZipPackagePathEnabled( self ) :
        self.optionsUnderTest.isZipFile = True
        self.optionsUnderTest.output = 'some/path'
        self.optionsUnderTest.package = 'package-name'

        expectedPath = os.path.join( self.optionsUnderTest.output, '{0}.zip'.format( self.optionsUnderTest.package ) )

        self.assertEqual( expectedPath, self.optionsUnderTest.zipPackagePath )


    def testZipPackagePathDisabled( self ) :
        self.optionsUnderTest.isZipFile = False

        self.assertIsNone( self.optionsUnderTest.zipPackagePath )


if __name__ == '__main__' :
    unittest.main()
