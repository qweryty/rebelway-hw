from typing import Optional
import hou


def print_nodes(head: hou.OpNode) -> None:
    current = head
    while current.outputs():
        print(current.name())
        current = current.outputs()[0]

    print(current.name())  # Don't forget the tail node


def find_tail(head: hou.OpNode) -> hou.OpNode:
    current = head
    while current.outputs():
        current = current.outputs()[0]

    return current


def insert_node(head: hou.OpNode, node: hou.OpNode, index: int) -> None:
    current = head
    if index < 0:
        raise IndexError("Index can't be negative")
    for _ in range(index):
        outputs = current.outputs()
        if not outputs:
            raise IndexError("Index is out of range")

        current = outputs[0]

    outputs = current.outputsWithIndices()
    child_node: Optional[hou.OpNode]
    if outputs:
        child_node, out_index, in_index = outputs[0]
    else:
        child_node = None
        out_index = 0
        in_index = 0
    node.setInput(0, current, output_index=out_index)
    if child_node is not None:
        child_node.setInput(in_index, node)
