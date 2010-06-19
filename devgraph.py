#!/usr/bin/python

import gudev
import os
import pygraphviz

cluster = False

g = pygraphviz.AGraph (directed = True)
#g.graph_attr.update (fontsize='9', fontname='Helvetica')
g.node_attr.update (fontsize='8')

def add_node (device):
    if cluster and device.get_subsystem ():
        sg = g.get_subgraph (device.get_subsystem ())
        if not sg:
            sg = g.add_subgraph (name='cluster_' + device.get_subsystem (), label = device.get_subsystem ())
    else:
        sg = g

    label = []
    if device.get_device_type () != gudev.DEVICE_TYPE_NONE:
        label.append (device.get_device_file ())
        if os.path.split (device.get_device_file ())[1] != device.get_name ():
            label.append ("'%s'" % device.get_name ())
    else:
        label.append (device.get_name ())

    label2 = []
    if (device.get_subsystem ()):
        label2.append (device.get_subsystem ())
    if device.get_devtype ():
        label2.append ('(%s)' % device.get_devtype ())
    if device.get_driver ():
        label2.append ('[%s]' % device.get_driver ())

    d = {}
    d['label'] = (' '.join (label)) + r'\n' + (' '.join (label2))
    d['shape'] = 'box'
    if device.get_device_type () != gudev.DEVICE_TYPE_NONE:
        d['style'] = 'filled'
    sg.add_node (device.get_sysfs_path (), **d)

    if device.get_parent ():
        if (not sg.has_node (device.get_parent ())):
            add_node (device.get_parent ())
        g.add_edge (device.get_sysfs_path (), device.get_parent ().get_sysfs_path ())

c = gudev.Client ([])
for device in c.query_by_subsystem (None):
    if not g.has_node (device.get_sysfs_path ()):
        add_node (device)
print g.to_string ()
