### DNNF Class

class DNNF:
    def __init__(self):
        ''' Constructor for this class. '''
        # Create internal data structure
        self.circuit = dict()
        self.topological_order = []
        self.node_counter = 0;
        self.root = None;

    def __repr__(self):
        ''' Conversion to a string. '''
        return str(self.circuit);


    def set_root(self, root_id):
        ''' Declare a node given by its id as the root of the circuit. '''
        self.root = root_id;
        return root_id;


    def add_node(self, node):
        ''' Add a literal node, last in the topological ordering. '''
        if not isinstance(node, Node):
            raise TypeError("can only add nodes of type Node")
        node_id = self.node_counter;
        self.circuit[node_id] = node;
        self.topological_order += [node_id];
        self.node_counter += 1;
        return node_id;


    def is_decomposable(self):
        ''' Check whether the NNF circuit is decomposable. '''
        # Go through the circuit (bottom up),
        # and for each node, compute what variables are below it
        # Plus: whenever you run into an And node,
        # check whether the variables below the children are pairwise disjoint
        subvars = dict();
        for node in self.topological_order:
            cur_node = self.circuit[node];
            if isinstance(cur_node, PosLit):
                subvars[node] = set([cur_node.variable]);
            elif isinstance(cur_node, NegLit):
                subvars[node] = set([cur_node.variable]);
            elif isinstance(cur_node, And):
                varsets = []
                for child in cur_node.children:
                    varsets += [[subvars[child]]];
                # Check if variables below children are pairwise disjoint
                vars = set();
                for varset in varsets:
                    if not vars.isdisjoint(varset[0]):
                        return False;
                    vars |= varset[0];
                subvars[node] = vars;
            elif isinstance(cur_node, Or):
                varsets = []
                for child in cur_node.children:
                    varsets += [[subvars[child]]];
                vars = set();
                for varset in varsets:
                    vars |= varset[0];
                subvars[node] = vars;
            elif isinstance(cur_node, Top):
                subvars[node] = set();
            elif isinstance(cur_node, Bot):
                subvars[node] = set();
        return True;


    def is_consistent(self):
        ''' Check whether the DNNF circuit is consistent. '''
        consistent = dict();
        for node in self.topological_order:
            cur_node = self.circuit[node];
            if isinstance(cur_node, PosLit):
                consistent[node] = True;
            elif isinstance(cur_node, NegLit):
                consistent[node] = True;
            elif isinstance(cur_node, And):
                defaultValue = True;
                for child in cur_node.children:
                    if consistent[child] == False:
                        defaultValue = False;
                consistent[node] = defaultValue;
            elif isinstance(cur_node, Or):
                defaultValue = False;
                for child in cur_node.children:
                    if consistent[child] == True:
                        defaultValue = True;
                consistent[node] = defaultValue;
            elif isinstance(cur_node, Top):
                consistent[node] = True;
            elif isinstance(cur_node, Bot):
                consistent[node] = False;
        return consistent[self.root];


    def condition(self, assignment):
        ''' Condition the DNNF circuit on a given truth assignment. '''
        for node in self.topological_order:
            cur_node = self.circuit[node];
            if isinstance(cur_node, PosLit):
                if assignment.get(cur_node.variable) == False:
                    self.circuit[node] = Bot();
                elif assignment.get(cur_node.variable) == True:
                    self.circuit[node] = Top();
            elif isinstance(cur_node, NegLit):
                if assignment.get(cur_node.variable) == True:
                    self.circuit[node] = Bot();
                elif assignment.get(cur_node.variable) == False:
                    self.circuit[node] = Top();
        # perform simplification (TODO)
        return;


    def simplify(self):
        ''' Simplify the DNNF circuit:
        - Remove unary And/Or nodes (and reconnect the circuit appropriately)
        - Propagate Bot/Top nodes through And/Or nodes
        - Ensure that there is at most one occurrence of each literal
        - Remove nodes that are unreachable from the root'''
        # Keep track of a remapping for nodes,
        # a list of nodes to delete,
        # and a mapping of seen literals to their nodes
        node_remapping = dict();
        nodes_to_remove = [];
        literals_and_constants = dict();
        # Go through the circuit in order
        for node in self.topological_order:
            cur_node = self.circuit[node];
            # Case 1: And node
            if isinstance(cur_node, And):
                # Repeat simplification steps for as long as necessary
                # (i.e., until nothing changes anymore)
                repeat = True;
                while repeat == True:
                    repeat = False;
                    # If node has no children, it's a Top
                    if len(cur_node.children) == 0:
                        self.circuit[node] = Top();
                    # If node has 1 child, it becomes the child
                    elif len(cur_node.children) == 1:
                        child = cur_node.children[0];
                        remap = node_remapping.get(child);
                        if remap == None:
                            remap = child;
                        node_remapping[node] = remap;
                        nodes_to_remove += [node];
                    # If it has >1 children, go through the list
                    else:
                        contains_bot = False;
                        children_to_remove = [];
                        for i in range(0,len(cur_node.children)):
                            # If a child is Bot, entire And node becomes Bot
                            if isinstance(self.circuit[cur_node.children[i]],Bot):
                                contains_bot = True;
                            # If a child is Top, it can be deleted
                            if isinstance(self.circuit[cur_node.children[i]],Top):
                                children_to_remove += [cur_node.children[i]];
                            # Do remapping on children
                            remap = node_remapping.get(cur_node.children[i]);
                            if remap != None:
                                cur_node.children[i] = remap;
                        # Update list of children,
                        # and mark if another repetition is needed
                        new_children = list(set(cur_node.children));
                        for child in children_to_remove:
                            new_children.remove(child);
                        if len(new_children) < len(cur_node.children):
                            repeat = True;
                        cur_node.children = new_children;
                        if contains_bot:
                            self.circuit[node] = Bot();
            # Case 2: Or node
            elif isinstance(cur_node, Or):
                # Repeat simplification steps for as long as necessary
                # (i.e., until nothing changes anymore)
                repeat = True;
                while repeat == True:
                    repeat = False;
                    # If node has no children, it's a Bot
                    if len(cur_node.children) == 0:
                        self.circuit[node] = Bot();
                    # If node has 1 child, it becomes the child
                    elif len(cur_node.children) == 1:
                        child = cur_node.children[0];
                        remap = node_remapping.get(child);
                        if remap == None:
                            remap = child;
                        node_remapping[node] = remap;
                        nodes_to_remove += [node];
                    # If it has >1 children, go through the list
                    else:
                        contains_top = False;
                        children_to_remove = [];
                        for i in range(0,len(cur_node.children)):
                            # If a child is Top, entire And node becomes Top
                            if isinstance(self.circuit[cur_node.children[i]],Top):
                                contains_top = True;
                            # If a child is Bot, it can be deleted
                            if isinstance(self.circuit[cur_node.children[i]],Bot):
                                children_to_remove += [cur_node.children[i]];
                            # Do remapping on children
                            remap = node_remapping.get(cur_node.children[i]);
                            if remap != None:
                                cur_node.children[i] = remap;
                        # Update list of children,
                        # and mark if another repetition is needed
                        new_children = list(set(cur_node.children));
                        for child in children_to_remove:
                            new_children.remove(child);
                        if len(new_children) < len(cur_node.children):
                            repeat = True;
                        cur_node.children = new_children;
                        if contains_top:
                            self.circuit[node] = Top();
            # Case 3: literals
            # Check if this literal has already been encountered;
            # if so, replace it by the previous occurrence, otherwise, keep track of it
            elif isinstance(cur_node, PosLit) or isinstance(cur_node, NegLit):
                new_literal = literals_and_constants.get(str(cur_node));
                if new_literal != None:
                    node_remapping[node] = new_literal;
                    nodes_to_remove += [node];
                else:
                    literals_and_constants[str(cur_node)] = node;
        # Remove all nodes that have been marked for deletion
        nodes_to_remove = list(set(nodes_to_remove));
        for node in nodes_to_remove:
            self.circuit.pop(node);
            self.topological_order.remove(node);
        # Update the root node
        new_root = node_remapping.get(self.root);
        if new_root == None:
            new_root = self.root;
        self.root = new_root;
        # Go through the circuit and compute all nodes that are
        # reachable (in reverse) from the root.
        # Then delete all nodes that are not reachable.
        reached = [self.root];
        handled = [];
        while reached != []:
            node = reached[0];
            reached.remove(node);
            handled += [node];
            cur_node = self.circuit[node];
            if isinstance(cur_node, And):
                for child in cur_node.children:
                    if not child in handled:
                        reached += [child];
            if isinstance(cur_node, Or):
                for child in cur_node.children:
                    if not child in handled:
                        reached += [child];
        nodes_to_remove = set(self.topological_order) - set(handled);
        for node in nodes_to_remove:
            self.circuit.pop(node);
            self.topological_order.remove(node);


    # TODOs:
    # - add WMM conditioning


    def write_to_file(self, filename):
        ''' Writes the DNNF to a file in NNF format '''
        # Compute the number of nodes, edges, and variables
        numnodes = len(self.topological_order);
        numedges = 0;
        maxvar = 0;
        for node in self.topological_order:
            cur_node = self.circuit[node];
            if isinstance(cur_node, And) or isinstance(cur_node, Or):
                numedges += len(cur_node.children);
            elif isinstance(cur_node, PosLit) or isinstance(cur_node, NegLit):
                var = int(cur_node.variable);
                if var > maxvar:
                    maxvar = var;
        # Write the file representation of the DNNF
        file = open(filename,"w");
        file.write("nnf "+str(numnodes)+" "+str(numedges)+" "+str(maxvar)+"\n");
        line_mapping = dict();
        current_line = 0;
        for node in self.topological_order:
            line_mapping[node] = current_line;
            cur_node = self.circuit[node];
            if isinstance(cur_node, PosLit):
                file.write("L "+str(cur_node.variable)+"\n");
            elif isinstance(cur_node, NegLit):
                file.write("L -"+str(cur_node.variable)+"\n");
            elif isinstance(cur_node, And):
                file.write("A "+str(len(cur_node.children))+" "+" ".join(map(str,cur_node.children))+"\n");
            elif isinstance(cur_node, Or):
                file.write("O "+str(len(cur_node.children))+" "+" ".join(map(str,cur_node.children))+"\n");
            elif isinstance(cur_node, Top):
                file.write("A 0\n");
            elif isinstance(cur_node, Bot):
                file.write("O 0\n");
            current_line += 1;
        file.close();


    def read_from_file(filename):
        ''' Reads the DNNF from a file in NNF format '''
        file = open(filename, "r");
        first_line = file.readline();
        outDNNF = DNNF();
        current_line = 0;
        line_to_node_mapping = dict();
        for line in file:
            symbols = line[0:-1].split(" ");
            print(symbols);
            # Literals
            if symbols[0] == 'L':
                if symbols[1][0] == '-':
                    # Negative literal
                    node = outDNNF.add_node(NegLit(int(symbols[1][1:])));
                else:
                    # Positive literal
                    node = outDNNF.add_node(PosLit(int(symbols[1])));
            # And node
            elif symbols[0] == 'A':
                children = []
                for line in symbols[2:]:
                    children += [line_to_node_mapping[int(line)]];
                node = outDNNF.add_node(And(children));
            # Or node
            elif symbols[0] == 'O':
                children = []
                for line in symbols[2:]:
                    children += [line_to_node_mapping[int(line)]];
                node = outDNNF.add_node(Or(children));
            line_to_node_mapping[current_line] = node;
            current_line += 1;
        outDNNF.set_root(current_line-1);
        return outDNNF;


### Classes for nodes of the circuit

class Node:
    def __init__(self):
        ''' Constructor for this class. '''
    def __repr__(self):
        ''' Conversion to a string. '''
        return "Node";

class And(Node):
    def __init__(self, children):
        ''' Constructor for this class. '''
        self.children = children;
    def __repr__(self):
        ''' Conversion to a string. '''
        return f"And({self.children})";

class Or(Node):
    def __init__(self, children):
        ''' Constructor for this class. '''
        self.children = children;
    def __repr__(self):
        ''' Conversion to a string. '''
        return f"Or({self.children})";

class PosLit(Node):
    def __init__(self, variable):
        ''' Constructor for this class. '''
        self.variable = variable;
    def __repr__(self):
        ''' Conversion to a string. '''
        return f"Lit({self.variable})";

class NegLit(Node):
    def __init__(self, variable):
        ''' Constructor for this class. '''
        self.variable = variable;
    def __repr__(self):
        ''' Conversion to a string. '''
        return f'Lit(-{self.variable})';

class Top(Node):
    def __init__(self):
        ''' Constructor for this class. '''
    def __repr__(self):
        ''' Conversion to a string. '''
        return "True";

class Bot(Node):
    def __init__(self):
        ''' Constructor for this class. '''
    def __repr__(self):
        ''' Conversion to a string. '''
        return "False";
