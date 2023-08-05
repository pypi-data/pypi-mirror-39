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
This file is part of tendril
See the COPYING, README, and INSTALL files for more information
"""

import atexit

try:
    from tendril.devtooling import stacktracer
    stacktracer.trace_start("trace.html")
    atexit.register(stacktracer.trace_stop)
except ImportError:
    stacktracer = None

from tendril.frontend.app import app
from tendril.frontend.startup.init_app import init_app

init_app(app)
app.use_x_sendfile = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
