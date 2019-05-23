from maya import cmds
import ast

def create_message_attr_setup(out_node, out_message_attr_name, in_node, in_message_attr_name ):
    # adds a message attr to out_node, adds message attr to in_node connects out message attr to the in message attr
    out_attr_fullname = out_node + "." + out_message_attr_name
    in_attr_fullname = in_node + "." + in_message_attr_name
    if not cmds.objExists(out_attr_fullname):
        cmds.addAttr(out_node, ln=out_message_attr_name, attributeType="message")
    if not cmds.objExists(in_attr_fullname):
        cmds.addAttr(in_node, ln=in_message_attr_name, attributeType="message")
    cmds.connectAttr(out_attr_fullname, in_attr_fullname, f=True)
    return out_attr_fullname, in_attr_fullname


def get_node_from_message(full_attr_name, from_output = True, get_single=True):
    source = False
    destination = True
    if not from_output:
        source = True
        destination = False
    if not cmds.objExists(full_attr_name):
        return
    connections = cmds.listConnections(full_attr_name, shapes=True, source=source, destination=destination)
    if not connections:
        return
    if get_single:
        return connections[0]
    return connections


def get_nodes_from_message(nodes, attr_name, from_output = True, get_single=False):
    return_nodes = []
    for node in nodes:
        full_attr_name = node + "." + attr_name
        if not cmds.objExists(full_attr_name):
            continue
        return_nodes.append(get_node_from_message(full_attr_name, from_output = from_output, get_single=get_single))
    return return_nodes


def get_node_from_message_out(full_attr_name, get_single=True):
    return get_node_from_message(full_attr_name, from_output = True, get_single=get_single)


def get_node_from_message_in(full_attr_name, get_single=True):
    return get_node_from_message(full_attr_name, from_output = False, get_single=get_single)


# Not necessarily a message attr, but this will contain dictionaries of information about connections
# To retrieve dictionaries stored as strings:
# ast.literal_eval("{"DICTIONARY_KEY":["thingA", "thingB"]}")
def string_array_for():
    return