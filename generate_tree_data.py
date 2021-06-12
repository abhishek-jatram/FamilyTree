from generate_tree import FamilyTree
import json

ftree = FamilyTree('data.csv')

def pre_order_traversal(node_id):
    node_data = dict()
    if node_id in ftree.data.keys():
        node_data['name'] = ftree.data[node_id]['name']
        node_data['gender'] = ftree.data[node_id]['gender']
        node_data['dob'] = ftree.data[node_id]['dob']
    
    if node_id in ftree.tree.keys():
        node_data['children'] = list()
        for child_id in ftree.tree[node_id]:
            node_data['children'].append(pre_order_traversal(child_id))
    return node_data

tree_data = pre_order_traversal(0)
#json_data = json.dumps(tree_data)
#print(json_data)
with open('data.js','w') as file:
    json.dump(tree_data, file, indent=2, separators=(', ', ': '), sort_keys=False)

lines = ['var treeData = ']
with open('data.js', 'r') as file:
    lines += file.readlines()

with open('data.js', 'w') as file:
    file.writelines(lines)