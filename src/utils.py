from abc import ABC, abstractmethod
import json
import argparse

# 节点类
class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def show(self, prefix="", is_last=True):
        pass

# 中间节点类
class IntermediateNode(Node):
    def __init__(self, name, icon):
        super().__init__(name)
        self.icon = icon
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def show(self, prefix="", is_last=True):
        print(prefix + ('└─ ' if is_last else '├─ ') + self.icon + ' ' + self.name)
        prefix += '    ' if is_last else '│   '
        # spacing = "    "
        # prefix += spacing if is_last else '│' + spacing[1:]
        for i, child in enumerate(self.children):
            child.show(prefix, i == len(self.children) - 1)



# 叶子节点类
class LeafNode(Node):
    def __init__(self, name, icon):
        super().__init__(name)
        self.icon = icon

    def show(self, prefix="", is_last=True):
        print(prefix + ('└─ ' if is_last else '├─ ') + self.icon + ' ' + self.name)

# 图标族抽象工厂   使用 @abstractmethod 装饰器来定义抽象方法，这些方法在子类中必须被实现。因为python中没有interface关键字，因此用ABC来实现
class IconFactory(ABC):
    # @abstractmethod
    # def create_node(self,name,node_kind,icons):
    #     pass

    @abstractmethod
    def create_intermediate_node(self, name, icons):
        pass

    @abstractmethod
    def create_leaf_node(self, name, icons):
        pass

# 具体图标族工厂
class SimpleIconFactory(IconFactory):
    # def create_node(self,name,node_kind,icons=None):
    #     if node_kind=="inter":
    #         return IntermediateNode(name,'')
    #     if node_kind=="leaf":
    #         return LeafNode(name,'')

    def create_intermediate_node(self, name, icons=None):
        return IntermediateNode(name, '')

    def create_leaf_node(self, name, icons=None):
        return LeafNode(name,'')

class PokerFaceFactory(IconFactory):
    # def create_node(self, name, node_kind,icons=None):
    #     if node_kind == "inter":
    #         return IntermediateNode(name, '♢')
    #     if node_kind == "leaf":
    #         return LeafNode(name, '♤')

    def create_intermediate_node(self, name, icons=None):
        return IntermediateNode(name, '')

    def create_leaf_node(self, name, icons=None):
        return LeafNode(name, '')



class Builder(ABC):
    @abstractmethod
    def build(self, json_data):
        pass

class TreeBuilder(Builder):
    def __init__(self, icon_factory):
        self.icon_factory = icon_factory
        self.root=None

    def build(self, json_data):
        self.root = IntermediateNode('root', '')
        self.build_recursive(json_data, self.root)
        return self.root

    def build_recursive(self, json_data, parent_node):
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if value is None:
                    # 如果值是 None，添加叶子节点，只包含键的名字
                    leaf_node = self.icon_factory.create_leaf_node(key)
                    parent_node.add_child(leaf_node)
                elif isinstance(value, (dict, list)):
                    child_node = self.icon_factory.create_intermediate_node(key)
                    parent_node.add_child(child_node)
                    self.build_recursive(value, child_node)
                else:
                    leaf_node = self.icon_factory.create_leaf_node(f'{key}: {str(value)}')
                    parent_node.add_child(leaf_node)
        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                if item is None:
                    # 如果值是 None，添加叶子节点，只包含索引的名字
                    leaf_node = self.icon_factory.create_leaf_node(f'Item {i}')
                    parent_node.add_child(leaf_node)
                elif isinstance(item, (dict, list)):
                    child_node = self.icon_factory.create_intermediate_node(f'Item {i}')
                    parent_node.add_child(child_node)
                    self.build_recursive(item, child_node)
                else:
                    leaf_node = self.icon_factory.create_leaf_node(f'Item {i}: {str(item)}')
                    parent_node.add_child(leaf_node)
        else:
            if json_data is not None:
                leaf_node = self.icon_factory.create_leaf_node(str(json_data))
                parent_node.add_child(leaf_node)

    def show(self):
        for i, child in enumerate(self.root.children):
            child.show(prefix="", is_last=(i == len(self.root.children) - 1))


class RectangleBuilder(TreeBuilder):
    # position==0代表普通节点， position==1代表左上节点, position==2代表是最后一个孩子
    def show(self, node=None, prefix="", is_last=True, max_width=50, position=0):
        if node is None:
            node = self.root
        if isinstance(node, IntermediateNode):
            if position==1:
                line=prefix + '┌ ' + node.icon + ' ' + node.name
                if max_width > 0:
                    line += ' ' + '─' * (max_width - len(line))+'┐'
            else:
                # line=prefix + ('└─ ' if is_last else '├─ ') + node.icon + ' ' + node.name
                line = prefix + '├─ ' + node.icon + ' ' + node.name
                if max_width > 0:
                    line += ' ' + '─' * (max_width - len(line))+'┤'
            if(node!=self.root):
                print(line)
            # prefix += '    ' if is_last else '│   '
            if node!=self.root:
                prefix += '│   '
            for i, child in enumerate(node.children):
                if(node==self.root and i==0):
                    self.show()
                elif i==len(node.children)-1 and (position==2 or node==self.root):
                    self.show()
                else:
                    self.show()
        elif isinstance(node, LeafNode):
            if position==2:
                # 最后一行
                new_prefix='└'+ '─' * (len(prefix)-len('└'))
                line = new_prefix + '┴ ' + node.icon + ' ' + node.name
                if max_width > 0:
                    line += ' ' + '─' * (max_width - len(line)) + '┘'
            else:
                line = prefix + '├─ ' + node.icon + ' ' + node.name
                if max_width > 0:
                    line += ' ' + '─' * (max_width - len(line))+'┤'
                    prefix += '│   '
            if (node != self.root):
                print(line)


