import random

class Node:
    # colors = [(153,51,255),
    #           (51,51,255),
    #           (51,153,255),
    #           (51,255,255),
    #           (51,255,153),
    #           (51,255,51),
    #           (0,153,0),
    #           (255,255,0),
    #           (255,153,51),
    #           (255,51,51),
    #           (255,51,255)]

    def __init__(self):
        #random.shuffle(self.colors)
        #self.color = self.colors.pop(0)
        self.goal = False
        self.links = []



class Goal(Node):
    def __init__(self):
        super().__init__()
        self.goal = True
        self.color = (255,255,255)



class Graph:
    #trunk_nodes = []

    def __init__(self,depth=2):
        self.all_nodes = []
        self.trunk_nodes = []
        goalNode = Goal()
        self.trunk_nodes.append(goalNode)
        lastNode = goalNode
        for i in range(depth-1):
            #make a node
            node = Node()
            #link it
            self.add_node(node,self.trunk_nodes[-1:])

    def add_node(self,node,nodes=[]):
        if not nodes:
            return 0
        if not isinstance(node, Node):
            raise TypeError("Nodes required.")
        for anode in nodes:
            if not isinstance(anode, Node):
                raise TypeError("Nodes required")
            #if it already had links, that's complicated
            if anode.links and len(anode.links) >= 2:
                print("not implemented")
                return 0
            else:
                anode.links.append(node)
                node.links.append(anode)
                self.trunk_nodes.append(node)
                self.all_nodes.append(node)






#Test code
# for i in range(100):
#     a = Graph(depth=5)
#     print('test')


