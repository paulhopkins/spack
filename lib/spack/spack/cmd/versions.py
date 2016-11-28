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
from llnl.util.tty.colify import colify
import llnl.util.tty as tty
import spack
from ordereddict_backport import OrderedDict


description = "List available versions of a package"


def setup_parser(subparser):
    subparser.add_argument('package', metavar='PACKAGE',
                           help='Package to list versions for')
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="Don't clean up staging area when command completes.")

def versions(parser, args):
    pkg = spack.repo.get(args.package)

    safe_versions = pkg.versions
    fetched_versions = pkg.fetch_remote_versions()
    remote_versions = set(fetched_versions).difference(safe_versions)

    tty.msg("Safe versions (already checksummed):")
    colify(sorted(safe_versions, reverse=True), indent=2)

    tty.msg("Remote versions (not yet checksummed):")
    if not remote_versions:
        if not fetched_versions:
            print "  Found no versions for %s" % pkg.name
            tty.debug("Check the list_url and list_depth attribute on the "
                      "package to help Spack find versions.")
        else:
            print "  Found no unckecksummed versions for %s" % pkg.name
    else:
        colify(sorted(remote_versions, reverse=True), indent=2)

        # Fetch tarballs (prompting user if necessary)
        versions, urls = fetch_tarballs(pkg.url, pkg.name, sorted(remote_versions, reverse=True)[0])

        ver_hash_tuples = spack.cmd.checksum.get_checksums(
            versions, urls,
            keep_stage=args.keep_stage)
        
        if not ver_hash_tuples:
            tty.die("Could not fetch any tarballs for %s" % name)

        print make_version_calls(ver_hash_tuples)

def fetch_tarballs(url, name, version):
    """Try to find versions of the supplied archive by scraping the web.
    Prompts the user to select how many to download if many are found."""
    versions = spack.util.web.find_versions_of_archive(url)
    rkeys = sorted(versions.keys(), reverse=True)
    versions = OrderedDict(zip(rkeys, (versions[v] for v in rkeys)))

    archives_to_fetch = 1
    if not versions:
        # If the fetch failed for some reason, revert to what the user provided
        versions = {version: url}
    elif len(versions) > 1:
        tty.msg("Found %s versions of %s:" % (len(versions), name),
                *spack.cmd.elide_list(
                    ["%-10s%s" % (v, u) for v, u in versions.iteritems()]))
        print
        archives_to_fetch = tty.get_number(
            "Include how many checksums in the package file?",
            default=5, abort='q')

        if not archives_to_fetch:
            tty.die("Aborted.")

    sorted_versions = sorted(versions.keys(), reverse=True)
    sorted_urls = [versions[v] for v in sorted_versions]
    return sorted_versions[:archives_to_fetch], sorted_urls[:archives_to_fetch]

def make_version_calls(ver_hash_tuples):
    """Adds a version() call to the package for each version found."""
    max_len = max(len(str(v)) for v, h in ver_hash_tuples)
    format = "    version(%%-%ds, '%%s')" % (max_len + 2)
    return '\n'.join(format % ("'%s'" % v, h) for v, h in ver_hash_tuples)
