# Project Refactoring

## Image/Model

When modifying, ensure that no nodes using the Image/Model are overlooked.

> [!TIP]
>
> Make good use of global search.

## Pipeline

### Sub Node

Here, nodes with the deprecated `is_sub` value set to `true` are referred to as `sub nodes`.

Refactoring `sub nodes` involves the following steps:

1. Determine whether the `sub node` is of the lowest priority in the `next` list of the current node (i.e., directly moving it to the `interrupt` list of the current node has no impact on the actual effect).
2. If the `sub node` is not of the lowest priority, the refactoring method is to add the `next` and `interrupt` of the current node to the `sub node` (if the original `next` and `interrupt` are empty, this can be done directly; otherwise, consider potential conflicts). If the `sub node` is of the lowest priority, the refactoring method is to directly move it to the `interrupt` of the current node.
3. If the `sub node` is not of the lowest priority and the changes in step 2 cause conflicts, reconsider the task logic.
4. Remove the `is_sub` attribute from the `sub node`.

> [!WARNING]
>
> All the above changes must consider all nodes using the `sub node`. Do not overlook any!

### Other Nodes

Next, refactor other nodes based on their specific purposes.

#### Standardizing Node Names

If the goal is merely to standardize node names, use VSCode's global search and replace functionality.  
However, ensure that replacements include double quotes to avoid modifying other nodes containing the node name.

#### Simplifying Task Flows and Reducing Coupling

First, read [Node Connections](./Writing-Pipelines.md#node-connections) and refactor towards adhering to connection principles.

Some nodes can be moved to the `interrupt` of the ancestor node of the current node.  
After moving, remove unnecessary `next` nodes to avoid continuing the main task chain in the `interrupt`, which could cause errors in subsequent tasks and return to the ancestor node.

#### Merging Nodes with Similar Functions

If multiple nodes perform the same function, consider merging them into a single node.

Steps:

1. Before merging, check whether there are unrelated nodes in the `next` of the node. If so, separate them first.
2. During merging, all nodes should adopt the same standardized name.
3. After merging, check whether the node's position in all tasks is correct. For example, ensure nodes that should be in the `interrupt` are not in the main task chain's `next` section.
