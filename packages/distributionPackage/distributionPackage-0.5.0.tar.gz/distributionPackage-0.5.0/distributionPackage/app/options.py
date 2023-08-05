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
User specified packaging options.
"""

import os


class PackageOptions :
    """
    Collect parsed argument values, producing "composited" values such as file paths as necessary.
    """


    def __init__( self,
                  parsedArguments = None ) :
        self.append = None
        self.manifest = None
        self.output = None
        self.package = None
        self.projectRoot = None
        self.isTarFile = None
        self.isZipFile = None

        if parsedArguments is not None :
            self.append = parsedArguments.append
            self.manifest = parsedArguments.manifest
            self.output = parsedArguments.output
            self.package = parsedArguments.package
            self.projectRoot = parsedArguments.projectRoot
            self.isTarFile = parsedArguments.buildTar
            self.isZipFile = parsedArguments.buildZip


    @property
    def manifestPath( self ) :
        return self.manifest


    @property
    def tarPackagePath( self ) :
        if self.isTarFile :
            packagePath = os.path.join( self.output, '{0}.tar.gz'.format( self.package ) )
        else :
            packagePath = None

        return packagePath


    @property
    def zipPackagePath( self ) :
        if self.isZipFile :
            packagePath = os.path.join( self.output, '{0}.zip'.format( self.package ) )
        else :
            packagePath = None

        return packagePath
