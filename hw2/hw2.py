from typing import List
from dataclasses import dataclass, field
import hou

DATA = ["apple", "appricot", "pineapple", "pine", "pear", "banana"]


@dataclass
class TrieNode:
    char: str
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    root: TrieNode

    def __init__(self, data: List[str]):
        self.root = TrieNode(char="")
        for line in data:
            self.insert(line)

    def insert(self, line: str):
        current = self.root
        for c in line:
            if c not in current.children:
                current.children[c] = TrieNode(char=c)
            current = current.children[c]
        current.is_end = True

    def search(self, line: str) -> List[str]:
        current = self.root
        for c in line:
            if c not in current.children:
                return []
            current = current.children[c]

        return self._dfs(current, line[:-1], [])

    @classmethod
    def _dfs(cls, node: TrieNode, prefix: str, output: List[str]):
        prefix = prefix + node.char
        if node.is_end:
            output.append(prefix)

        for child in node.children.values():
            cls._dfs(child, prefix, output)

        return output


TRIE = Trie(DATA)


def execute():
    search_entry = hou.pwd().parm("search_entry").eval()
    print(TRIE.search(search_entry))
