# Copyright (C) 2015 Chintalagiri Shashank
#
# This file is part of Tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
gEDA Project File module documentation (:mod:`gedaif.projfile`)
===============================================================
"""

from . import conffile
import os


class GedaProjectFile(object):

    def __init__(self, projectfolder):
        self._projectfolder = projectfolder
        self.schfiles = []
        self.pcbfile = None
        self.configsfile = conffile.ConfigsFile(self._projectfolder)
        projfilepath = os.path.join(self.configsfile.schfolder,
                                    self.configsfile.projectfile)
        with open(projfilepath, 'r') as f:
            for line in f:
                line = self.strip_line(line)
                if line != '':
                    parts = line.split()
                    if parts[0].strip() == 'schematics':
                        self.schfiles = [x.strip() for x in parts[1:]]
                    if parts[0].strip() == 'output-name':
                        self.pcbfile = parts[1].strip().split('/')[-1]

    @staticmethod
    def strip_line(line):
        line = line.split("#")[0]
        return line.strip()

    @property
    def schpaths(self):
        return [os.path.join(self.configsfile.schfolder, schfile)
                for schfile in self.schfiles]


if __name__ == "__main__":
    pass
