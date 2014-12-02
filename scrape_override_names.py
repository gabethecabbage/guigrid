#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gbsgrid_back

prog_dict, prog_list = gbsgrid_back.find_sbgrid_progs()
override_ids = {}
for i in prog_list:
	override_ids[i] = gbsgrid_back.get_override_name(i)
	print i

print override_ids
