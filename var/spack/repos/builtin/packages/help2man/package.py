##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Help2man(AutotoolsPackage):
    """help2man is a script to create simple man pages from the --help and
--version output of programs."""

    homepage = "http://www.gnu.org/software/help2man/"
    url      = "https://ftp.gnu.org/gnu/help2man/help2man-1.47.4.tar.xz"

    version('1.47.4', '544aca496a7d89de3e5d99e56a2f03d3')
    version('1.47.3', 'd1d44a7a7b2bd61755a2045d96ecaea0')
    version('1.47.2', '5a171e903765da7d34b1810bbd69fec6')
