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
Test package options relating to manifest specification.
"""

import os
import unittest

from ..arguments import parseArguments


class TestManifestArgument( unittest.TestCase ) :

    def testDefaultManifest( self ) :
        """
        Manifest defaults
        """
        expectedDefaultManifestPath = 'manifest.yml'

        packageOptions = parseArguments( list() )

        actualManifestPath = packageOptions.manifestPath

        self.assertEqual( expectedDefaultManifestPath, actualManifestPath )


    def testShortFormManifest( self ) :
        """
        Short form manifest option.
        """
        manifestFile = 'some-manifest.yml'
        expectedManifestPath = manifestFile

        packageOptions = parseArguments( [ '-m', manifestFile ] )

        actualManifestPath = packageOptions.manifestPath

        self.assertEqual( expectedManifestPath, actualManifestPath )


    def testLongFormManifest( self ) :
        """
        Long form manifest option.
        """
        manifestFile = 'some-manifest.yml'
        expectedManifestPath = manifestFile

        packageOptions = parseArguments( [ '--manifest', manifestFile ] )

        actualManifestPath = packageOptions.manifestPath

        self.assertEqual( expectedManifestPath, actualManifestPath )


    def testManifestWithOutput( self ) :
        """
        The user specified manifest must be used independently of other arguments.
        """
        expectedManifestArgument = 'some/manifest.yml'
        outputArgument = 'another/path'

        inputArguments = [
            '-m',
            expectedManifestArgument,
            '-o',
            outputArgument,
        ]

        packageOptions = parseArguments( inputArguments )

        actualManifestPath = packageOptions.manifestPath

        self.assertEqual( expectedManifestArgument, actualManifestPath )


if __name__ == '__main__' :
    unittest.main()
