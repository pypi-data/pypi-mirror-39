import enum
import pathlib
import subprocess
import typing

class FilePathSource(enum.Enum):
	MERGE_BASE = "base"
	BASE = "our"
	HEAD = "their"

class ConflictingFile():
	def __init__(self, source:FilePathSource, mode:int, sha1:str, path:pathlib.Path) -> None:
		self.source = source
		self.mode = mode
		self.sha1 = sha1
		self.path = path

	@classmethod
	def parse(cls, line:str) -> "ConflictingFile":
		parts = line.split(None, 3)
		return cls(FilePathSource(parts[0]), int(parts[1]), parts[2], pathlib.Path(parts[3]))

	def __eq__(self, other:typing.Any) -> bool:
		if self.__class__ != other.__class__:
			return False
		return self.source == other.source and self.mode == other.mode and self.sha1 == other.sha1 and self.path == other.path

	def __repr__(self) -> str:
		return "%s: %s (%d, %s)" % (self.source, self.path, self.mode, self.sha1)

def find_conflicting_files(checkout_path:pathlib.Path, base_branch:str, head_branch:str) -> typing.List[typing.Dict[FilePathSource, ConflictingFile]]:
	result = [] # type: typing.List[typing.Dict[FilePathSource, ConflictingFile]]
	merge_base = subprocess.check_output(["git", "merge-base", base_branch, head_branch], cwd=str(checkout_path)).strip()
	attempted_merge = subprocess.check_output(["git", "merge-tree", merge_base, base_branch, head_branch], cwd=str(checkout_path)).decode("utf-8")
	attempted_merge_lines = attempted_merge.split("\n")
	for i in range(0, len(attempted_merge_lines)):
		if attempted_merge_lines[i] == "changed in both":
			conflict = {}
			for delta in range(1, len(FilePathSource) + 1):
				conflicting_file = ConflictingFile.parse(attempted_merge_lines[i + delta])
				conflict[conflicting_file.source] = conflicting_file
			result += [conflict]
	return result
