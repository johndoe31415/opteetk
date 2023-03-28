#	opteetk - Tools for easier debugging of OP-TEE
#	Copyright (C) 2023-2023 Johannes Bauer
#
#	This file is part of opteetk.
#
#	opteetk is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	opteetk is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with opteetk; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import gdb
import sys
import json
import uuid
import time

debug_session_id = uuid.uuid4()

def register_gdb(cmdclass):
	cmdclass()
	return cmdclass

def get_pager_structure():
	tee_pager_pmem_head = gdb.lookup_symbol("tee_pager_pmem_head")[0]
	first = int(tee_pager_pmem_head.value()["tqh_first"])
	current = first
	t_struct_tee_pager_pmem_ptr = gdb.lookup_type("struct tee_pager_pmem").pointer()
	pager_entries = [ ]
	while current != 0:
		entry = gdb.Value(current).cast(t_struct_tee_pager_pmem_ptr).dereference()
		pager_entries.append({
			"fobj_pgidx": int(entry["fobj_pgidx"]),
			"fobj": int(entry["fobj"]),
			"va_alias": int(entry["va_alias"]),
		})
		current = int(gdb.Value(current).cast(t_struct_tee_pager_pmem_ptr).dereference()["link"]["tqe_next"])
	return pager_entries


@register_gdb
class OpteePgtblDumpCommand(gdb.Command):
	def __init__ (self):
		gdb.Command.__init__(self, "optee-pgtbl-dump", gdb.COMMAND_USER)

	def invoke(self, arg, from_tty):
		entry = {
			"pager_struct": get_pager_structure(),
			"ts": time.time(),
			"sid": str(debug_session_id),
		}
		with open("/tmp/optee-pgtbl-dump.txt", "a") as f:
			json.dump(entry, f)
			f.write("\n")



@register_gdb
class OpteePgtblAutoDumpCommand(gdb.Command):
	def __init__ (self):
		gdb.Command.__init__(self, "optee-pgtbl-autodump", gdb.COMMAND_USER)

	def invoke(self, arg, from_tty):
		bp = gdb.Breakpoint("tee_pager_handle_fault")
		bp.commands = "\n".join([
			"optee-pgtbl-dump",
			"c",
			"", ])

#print("OP-TEE trace commands enabled.", file = sys.stderr)
print("OP-TEE trace commands enabled.")
