import nest

a = nest.Create("iaf_cond_exp", n=5)

nest.Connect(a, a, 'all_to_all', {"model": "static_synapse_lbl", "synapse_label": 123})
nest.Connect(a, a, 'all_to_all', {"model": "static_synapse_lbl", "synapse_label": 456})

print("a", len(nest.GetConnections(source=a, target=a, synapse_label=123)))
print("b", len(nest.GetConnections(target=a, synapse_label=123)))
print("c", len(nest.GetConnections(source=a, synapse_label=123)))

print("a", len(nest.GetConnections(source=a, target=a, synapse_label=456)))
print("b", len(nest.GetConnections(target=a, synapse_label=456)))
print("c", len(nest.GetConnections(source=a, synapse_label=456)))
