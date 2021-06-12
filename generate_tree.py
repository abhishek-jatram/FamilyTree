import pprint
import sys
import matplotlib.pyplot as plt

class TreeRender:
  radius = 1
  def __init__(self, start_year, end_year, width):
    fig = plt.figure(figsize=(20, 15))
    self.ax = fig.add_subplot(111)
    plt.xlim(0, width+10)
    plt.xticks([])
    plt.ylim(end_year + 5, start_year - 5)

  def node(self, x, y, info):
    x *= 1
    color = '#6ed5f5' if info['gender'] is 'M' else  'pink'
    # c_node = plt.Circle((x,y), radius=self.radius, color=color)
    # self.ax.add_patch(c_node)
    # plt.text(x, y+2, info['name'], ha='center', va= 'bottom',fontsize=11)
    self.ax.text(x, y, info['name'], color='black', ha='center', va='center', fontsize=11,
        bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.3,rounding_size=0.5'))

  def edge(self, x1, y1, x2, y2):
    x = (x1, x2)
    y = (y1, y2)
    plt.plot(x, y, 'k-', linewidth=1)

  def text(self, x, y, text, fontsize=8):
    plt.text(x, y, text, ha='center', va= 'bottom',fontsize=fontsize)

#data.csv
# ID,Name,DOB,Gender,ParentID
# 1,Name,1920,M,0

class FamilyTree:
  data = dict()
  tree = dict()
  def read_data(self, data_path):
    lines = open(data_path).read().split('\n')[:-1]
    for line in lines[1:]:
      id, name, dob, gender, parent_id = line.split(',')
      id = int(id)
      parent_id = int(parent_id)
      dob = int(dob)
      if(id in self.data.keys()):
        sys.exit('Duplicate IDs found. Please recheck the data file')

      self.data[id] = dict()
      self.data[id]['name'] = name
      self.data[id]['dob'] = dob
      self.data[id]['gender'] = gender
      self.data[id]['parent_id'] = parent_id

    for id in self.data.keys():
      if(self.data[id]['parent_id'] and 
         self.data[id]['parent_id'] not in self.data.keys()):
        sys.exit("Parent ID not found. Please recheck the data file")
    max_id = max(self.data.keys())

  def generate_tree(self):
    for id in self.data.keys():
      pid = self.data[id]['parent_id']
      if(pid not in self.tree.keys()):
        self.tree[pid] = list()
      self.tree[pid].append(id)

    def compare(id1, id2):
      return 1 if (self.data[id1]['dob'] > self.data[id2]['dob']) else -1
         
    for id in self.tree.keys():
      self.tree[id] = sorted(self.tree[id], cmp=compare)


  def __init__(self, data_path):
    self.read_data(data_path)
    self.generate_tree()
      
  def __str__(self):
    return pprint.pformat(self.data) + '\n' + pprint.pformat(self.tree)

  def post_order_traversal(self, node_id, dist, dist_of):
    if(node_id not in self.tree.keys()): #is a leaf node
      dist += 20
      dist_of[node_id] = dist 
      return dist
    else:
      width = 0
      for child_id in self.tree[node_id]:
        child_dist = self.post_order_traversal(child_id, dist + width, dist_of)
        width = child_dist - dist
      if len(self.tree[node_id]) > 1:
        dist_of[node_id] = dist + 10 + width / 2 
      else:
        dist_of[node_id] = dist + width
      return dist + width

  def get_node_positions(self):
    dist_of = dict()
    width = self.post_order_traversal(0, 10, dist_of)
    position = dict()
    for node_id in self.data.keys():
      if node_id in dist_of.keys():
        position[node_id] = dist_of[node_id], self.data[node_id]['dob']
    return position, width + 10

  def show(self):
    start_year = 20000; end_year = 0
    ids = self.data.keys()
    for id in ids:
      start_year = min(start_year, self.data[id]['dob'])
      end_year   = max(end_year, self.data[id]['dob'])

    # for t in range(start_year, end_year):
    #   render.text(2, t, str(t))
      
    position,width = self.get_node_positions()
    render = TreeRender(start_year, end_year, width)

    for id in ids:
      render.node(position[id][0], position[id][1], self.data[id])
    
    for id in self.tree.keys():
      if(id != 0):
        for i,child_id in enumerate(self.tree[id]):
          render.edge(position[id][0], position[id][1], position[child_id][0], position[child_id][1])
          # add child number
          # p = 0.8
          # x = p * position[id][0] + (1.0 - p) * position[child_id][0]
          # y = p * position[id][1] + (1.0 - p) * position[child_id][1]
          # render.text(x,y,i+1)
    plt.show()

if __name__ == '__main__':
  ftree = FamilyTree('data.csv')
  print(ftree)
  ftree.show()


"""
Unused code

  def get_level_order(self):
    EOL = -2 #End Of Level
    NA  = -1
    q = [0, EOL]
    order = []
    dist_of = dict()
    level = 0
    valid_child_in_level = False
    dist = 0
    while len(q) != 0:
      node_id = q.pop(0)
      if(node_id == EOL):
        if(not valid_child_in_level):
          break
        valid_child_in_level = False
        dist = 0
        level += 1
        if(len(q) !=0):
          q.append(EOL)
        continue

      dist += 10
      if(node_id == NA):
        order.append((NA, level))
        q.append(NA)
        dist += 10
        q.append(NA)
        continue

      order.append((node_id,level))
      dist_of[node_id] = dist
      if(node_id not in self.tree.keys()):
        q.append(NA)
      else:
        for child_id in self.tree[node_id]:
          valid_child_in_level = True
          q.append(child_id)

    # Recompute dist of parent nodes from bottom to top
    max_level = level
    for i in range(len(order)-1, 0, -1):
      node = order[i]
      id = node[0]
      node_level = node[1]
      if id in self.tree.keys():
        avg_d = 0
        for child_id in self.tree[id]:
          avg_d += dist_of[child_id]
        dist_of[id] = avg_d / len(self.tree[id])
      elif id in dist_of.keys():
        dist_of[id] += 10*pow(2, max_level - node_level)
    return order,dist_of

  def print_level_order(self):
    order,dist_of = self.get_level_order()
    print order
    l = 0
    for node in order:
      if(l != node[1]):
        print "\n"
        l = node[1]
      print str(node[0]) + ":" + str(dist_of[node[0]] if node[0] > 0 else 0) + " ",

  def get_node_positions1(self):
    order,dist_of = self.get_level_order()
    NA = -1
    position = dict()
    for node in order:
      node_id = node[0]
      if(node_id != NA and node_id != 0):
        node_d  = dist_of[node_id]
        position[node_id] = node_d, self.data[node_id]['dob']
    return position
"""