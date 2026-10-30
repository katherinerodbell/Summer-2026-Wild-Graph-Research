#run in sagemath kernel

def find_wild_number(graph,set_or_number):
    if graph.is_connected()==False: #before we start, check if inputted graph is actually connected
        return "original graph is not connected"
    #colored graph generation
    from collections import defaultdict
    edges_by_color = defaultdict(list)
    for u, v, color in graph.edges():
        edges_by_color[color].append((u, v))
    colors = []
    for color, edges in edges_by_color.items():
        H = Graph()
        H.add_vertices(graph.vertices())   # keep all vertices
        H.add_edges(edges)                 # add only edges of this color
        colors.append(H)
    graph_edges = graph.edges(labels=False) #make a set of all edges to take combinations from
    wld = 0 #start with 0
    from itertools import combinations #needed function to generate combinations
    while True: #this loop goes through each possible wild edge set until one is found, which will be minimal as number of edges is increasing. it can't run forever, as it will eventually check the possibility the every edege is wild
        connected_colors = 0 #start connected colors at zero
        for trial_edge_set in (combinations(graph_edges, wld)): #for each combination of edges of the wild number currently being tested                        
            for k in colors: #for each color                
                if (k.union(Graph(list(trial_edge_set)))).is_connected()==True: #if the color combined with current wild edge set is connected                     
                    connected_colors += 1 #then we add to the connected counter                    
            if (connected_colors == len(colors)): #if every color is connected                    
                    if set_or_number == "set":
                        return trial_edge_set
                    elif set_or_number == "both":
                        print("wild set:") #output set
                        print(trial_edge_set)
                        print("wild number:") #output number
                        return wld
                    else:
                        return wld            
            else: #if we didn't have every color connected, reset for next wild number                
                connected_colors = 0 #reset connected colors, try next edge set            
        wld += 1 #once all edge sets of a certain number have been tried, if none worked, try the next number
        
def find_wild_sets(graph):
    if graph.is_connected()==False: #before we start, check if inputted graph is actually connected
        return "original graph is not connected"
    #beginning of colored graph generation
    from collections import defaultdict
    edges_by_color = defaultdict(list)
    for u, v, color in graph.edges():
        edges_by_color[color].append((u, v))
    colors = []
    for color, edges in edges_by_color.items():
        H = Graph()
        H.add_vertices(graph.vertices())   # keep all vertices
        H.add_edges(edges)                 # add only edges of this color
        colors.append(H)
    graph_edges = graph.edges(labels=False) #make a set of all edges to take combinations from
    wld = 0 #start with 0
    wld_sets = []
    from itertools import combinations #needed function to generate combinations
    while True: #this loop goes through each possible wild edge set until one is found, which will be minimal as number of edges is increasing. it can't run forever, as it will eventually check the possibility the every edege is wild   
        connected_colors = 0 #start connected colors at zero
        for trial_edge_set in (combinations(graph_edges, wld)): #for each combination of edges of the wild number currently being tested
            for k in colors: #for each color
                if (k.union(Graph(list(trial_edge_set)))).is_connected()==True: #if the color combined with curren wild edge set is connected    
                    connected_colors += 1 #then we add to the connected counter 
            if (connected_colors == len(colors)): #if every color is connected
                wld_sets.append(trial_edge_set)
                connected_colors = 0
            else: #if we didn't have every color connected, reset for next wild number
                connected_colors = 0 #reset connected colors, try next edge set
        if len(wld_sets)>0:
            return wld_sets
        else:
            wld += 1 #once all edge sets of a certain number have been tried, if none worked, try the next number
            
def edge_subsets(input_graph,n): #function which returns list of subsets of edges
    edge_count = len(input_graph.edges())
    if n == 2:
        pset = list(powerset(input_graph.edges()))
        pset_real = []
        for subset in pset:
            if (len(subset) != 0 and (len(subset) < edge_count/2)):
                pset_real.append(subset)
        print(len(pset_real), "edge combinations")
        return pset_real
    if n == 3:
        pset = list(powerset(input_graph.edges())) #make list of subsets
        pset_real = [] #make empty set for final output
        for subset in pset:
            if ((len(subset) >= edge_count/3) and (len(subset) <= edge_count-2)): #if no empty set will be created
                remainder = [item for item in input_graph.edges() if item not in subset] #define set difference of what's left for partition into two nonempty sets
                pset_jr = list(powerset(remainder)) #now do the n=2 process with "pset_jr" and each of its "subset_jr"s
                for subset_jr in pset_jr:
                    if (len(subset_jr) >= (edge_count - len(subset))/2) and (len(subset_jr) <= (edge_count - len(subset)-1)) and (len(subset) >= len(subset_jr)):
                        pset_real.append([]) #add a set to final outputs for this partition based on the current subset of the orignal edge set
                        pset_real[-1].append([]) #add a set to that set to put the edges in the current subset in
                        for edge in subset: 
                            pset_real[-1][-1].append(edge) #add them
                        pset_real[-1].append(subset_jr)
        print(len(pset_real), "edge combinations")
        return pset_real         
            
def bicolor(graph,subset): #bicolor a graph according to another graph (presumably a subset of its edges)
    for edge in graph.edges(): #remove all existing edge labels (important if coloring the same graph multiple times)
        graph.set_edge_label(edge[0],edge[1], None)
    for edge in graph.edges():
        if edge in subset:
            graph.set_edge_label(edge[0], edge[1] ,"blue")
        else:
            graph.set_edge_label(edge[0], edge[1],"red")
    return graph

def tricolor(graph,subsets): #tricolor a graph according to a set of three sets of edges
    for edge in graph.edges(): #remove all existing edge labels (important if coloring the same graph multiple times)
        graph.set_edge_label(edge[0],edge[1], None)
    for edge in graph.edges():
        if edge in subsets[0]:
            graph.set_edge_label(edge[0], edge[1],"blue")
        elif edge in subsets[1]:
            graph.set_edge_label(edge[0], edge[1],"red")
        else:
            graph.set_edge_label(edge[0], edge[1],"green")
    return graph

def display(coloring,color_number): #display a graph given a coloring and the number of colors in that coloring
    if color_number == 2:
        red_edges = []
        blue_edges = []
        for (u,v, Label) in coloring.edges():
            if Label == "blue": 
                blue_edges.append((u,v,Label))
            else:
                red_edges.append((u,v,Label))
        coloring.show(edge_colors={'red':red_edges, 'blue':blue_edges}, edge_labels=true, layout="circular")
    if color_number == 3:
        red_edges = []
        blue_edges = []
        green_edges = []
        for (u,v, Label) in coloring.edges():
            if Label == "blue": 
                blue_edges.append((u,v,Label))
            elif Label == "red":
                red_edges.append((u,v,Label))
            else:
                green_edges.append((u,v,"green"))
        coloring.show(edge_colors={"red":red_edges, "blue":blue_edges, "green":green_edges}, edge_labels=true, layout = "circular")
    
def histogram(list):
    from collections import Counter
    import matplotlib.pyplot as plt
    counts = Counter(list)
    frequencies = list(numbers.values())
    categories = list(numbers.keys())
    plt.bar(categories, frequencies)
    
def get_coloring_info(graph,number_of_colors): #returns a big list fo info about all unique colorings of a certain graph for a certain number of colors
    #make colorings
    colorings = []
    edge_sets = edge_subsets(graph,number_of_colors)    
    if number_of_colors == 2:
        for subset in edge_sets:
            temp_graph = graph.copy() 
            colorings.append(bicolor(temp_graph,subset))
    elif number_of_colors == 3:
        for subset in edge_sets:
            temp_graph = graph.copy() 
            colorings.append(tricolor(temp_graph,subset))
    #elif
    #other color counts go here eventually
    
    #find information about each coloring
    data = []
    for coloring in colorings:
        data.append([])
        data[-1].append(coloring) #edge list for recompiling into graph for potential visual display or filtering
        data[-1].append(number_of_colors)
        data[-1].append(find_wild_sets(coloring)) #wild sets (list)
        data[-1].append(len(data[-1][2])) #number of wild sets, found by taking the number of items in the list of wild sets
        data[-1].append(len(data[-1][2][0])) #wild number, found by taking length of a wild set    
    return data #a list of lists each containing a coloring, its number of colors, its minimal wild sets, its number of minimal wild sets, and its wild number

#def eliminate_redundancy(colorings):
#    aut_set = []
#    for coloring in colorings:
#        aut_set.append(coloring.automorphism_group())
#    for i in range(0,len(colorings),-1):
#        #if the previous elements contain a copy of the item in aut_set, remove the associated current item in the original set
#    return colorings
