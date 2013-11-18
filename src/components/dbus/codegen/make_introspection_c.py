#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @file make_introspection_c.py
#  @brief Converts introspection.xml to C-string
#
# This file is a part of HMI D-Bus layer.
# 
# Copyright (c) 2013, Ford Motor Company
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the
# distribution.
#
# Neither the name of the Ford Motor Company nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 'A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
for argv in sys.argv:
	if argv == "-h" or argv == "--help":
		print "This script converts introspection.xml to C-string\nInput: applink/src/components/interfaces/QT_HMI_API.xml"
		print "Output: applink/src/components/dbus/introspection.cc\n"
		exit("Exit from help. To run script don't use -h, --help")

from argparse import ArgumentParser
from ford_xml_parser import FordXmlParser
from ford_xml_parser import node_name
from xml.etree import ElementTree
from os import path
from sys import argv

class Impl(FordXmlParser):
    def convert_to_introspection(self, out_el_tree):
        for interface_el in self.el_tree.findall('interface'):
            el = self.create_introspection_iface_el(interface_el)
            if el is not None:
                out_el_tree.append(el)


arg_parser = ArgumentParser()
arg_parser.add_argument('--infile', required=True)
arg_parser.add_argument('--outdir', required=True)
args = arg_parser.parse_args()

if not path.isdir(args.outdir):
    makedirs(args.outdir)

out_file = open(args.outdir + '/' + 'introspection_xml.cc', "w")

in_tree = ElementTree.parse(args.infile)
in_tree_root = in_tree.getroot()
out_tree_root = ElementTree.Element('node', attrib={'name':node_name})

impl = Impl(in_tree_root, 'com.ford.hmi.sdl')
impl.convert_to_introspection(out_tree_root)

introspection_string = '<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN" "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">'
introspection_string += "\n"
introspection_string += ElementTree.tostring(out_tree_root)

out_file.write("// Warning! This file is generated by '%s'. Edit at your own risk.\n" % argv[0])
out_file.write("""/**
 * @file instrospections_xml.cc
 * @brief D-Bus introspection XML as C-string
 *
 * This file is a part of HMI D-Bus layer.
 */
// Copyright (c) 2013, Ford Motor Company
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// Redistributions of source code must retain the above copyright notice, this
// list of conditions and the following disclaimer.
//
// Redistributions in binary form must reproduce the above copyright notice,
// this list of conditions and the following
// disclaimer in the documentation and/or other materials provided with the
// distribution.
//
// Neither the name of the Ford Motor Company nor the names of its contributors
// may be used to endorse or promote products derived from this software
// without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 'A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

""")

out_file.write("char introspection_xml[] = {")

cnt = 0
for char in introspection_string:
    if cnt % 12 == 0:
        out_file.write("\n  ")
    else:
        out_file.write(" ")
    out_file.write("0x%02x," % ord(char))
    cnt = cnt + 1

out_file.write(" 0x00\n")
out_file.write("};")

