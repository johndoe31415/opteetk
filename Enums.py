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

import enum

class OpteeHeaderArch(enum.IntEnum):
	AArch32 = 0
	AArch64 = 1

class OpteeHeaderImageID(enum.IntEnum):
	Pager = 0
	Paged = 1
