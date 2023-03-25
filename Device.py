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

import json

class Device():
	def __init__(self, device_def: dict | None = None):
		if device_def is not None:
			self._def = device_def
		else:
			self._def = { }
		self._memory = self._parse_memories()

	@classmethod
	def parse_value(cls, text):
		if isinstance(text, int):
			return text
		elif isinstance(text, str):
			if text.endswith("k"):
				return 1024 * cls.parse_value(text[:-1])
			elif text.endswith("M"):
				return 1024 * 1024 * cls.parse_value(text[:-1])

			text = text.replace(" ", "")
			return int(text, 0)
		else:
			raise ValueError(f"Unsupported value: {text} type {type(text)}")

	def find_memory(self, address):
		for memory in self._memory:
			if memory["start"] <= address < memory["end"]:
				return memory
		return None

	def fmt_size(self, size):
		if size == 0:
			return "0"

		parts = [ ]
		if size >= 1024 * 1024:
			parts.append(f"{size // 1024 // 1024} MiB")
			size = size % (1024 * 1024)

		if size >= 1024:
			parts.append(f"{size // 1024} kiB")
			size = size % 1024

		if size > 0:
			parts.append(f"{size} B")
		return " + ".join(parts)

	def fmt_address(self, address):
		mem = self.find_memory(address)
		if mem is None:
			return f"{address:#x}"
		else:
			offset = address - mem["start"]
			bottom = mem["end"] - address
			if offset == 0:
				return f"{address:#x} (start of {self.fmt_size(mem['length'])} {mem['name']})"
			else:
				return f"{address:#x} (offset {self.fmt_size(offset)} into {self.fmt_size(mem['length'])} {mem['name']}, {self.fmt_size(bottom)} bytes left to end)"

	def dump(self):
		for memory in self._memory:
			print(f"Mem {memory['name']}: {mem['start']} - {mem['end']} (length {self.fmt_size(mem['length'])})")

	def _parse_memories(self):
		memories = [ ]
		for memory_def in self._def.get("memory", [ ]):
			start = self.parse_value(memory_def["start"])
			if "length" in memory_def:
				length = self.parse_value(memory_def["length"])
				end = start + length
			elif "end" in memory_def:
				end = self.parse_value(memory_def["end"])
				length = end - start
			parsed = {
				"name":		memory_def.get("name", "?"),
				"start":	start,
				"end":		end,
				"length":	length,
			}
			memories.append(parsed)
		return memories

	@classmethod
	def load_from_file(cls, filename):
		with open(filename) as f:
			return cls(device_def = json.load(f))
