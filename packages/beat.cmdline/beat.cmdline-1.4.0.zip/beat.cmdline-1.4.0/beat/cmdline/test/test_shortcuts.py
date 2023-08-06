#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.cmdline module of the BEAT platform.          #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################


import difflib

def test_shortcuts():
  shortcuts = {
      'c': 'config',
      'co': 'config',
      'cf': 'config',
      'st': 'status',
      's': 'status',
      'db': 'databases',
      'df': 'dataformats',
      'lib': 'libraries',
      'l': 'libraries',
      'algo': 'algorithms',
      'al': 'algorithms',
      'tc': 'toolchains',
      'exp': 'experiments',
      'xp': 'experiments',
  }

  for k, v in shortcuts.items():
    cmd = difflib.get_close_matches(k, set(shortcuts.values()), cutoff=0.2)
    assert len(cmd) > 0 and cmd[0] == v, "`%s' != `%s' (%s)" % (k, v, cmd[0])
