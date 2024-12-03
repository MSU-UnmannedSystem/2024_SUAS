import time
# Graph has x axis pointing down and y axis is pointing right

graph = {} #dictonary containing all verticies and edges
m, n = 5,5 # M: x-axis, N: y-axis
sq_cost = 0.5 #Battery drain per square
battery = 1 #Total battery percentage
LIMIT = 0.13
#Creates field of size m x n with False as the value to represent unvisited
field = [[False for _ in range(n)] for _ in range(m)]

'''
Test Field 1: top row and right column have been visited already
'''
temp_field = [[False for _ in range(n)] for _ in range(m)]
temp_set = set()
for i in range(n):
    temp_field[0][i] = True
    temp_set.add((0,i))
for i in range(m):
    temp_field[i][n-1] = True 
    temp_set.add(((i,n-1)))

'''
Test Field 2: More visited nodes to see how DFS behaves
'''
temp2_field = [[False for _ in range(n)] for _ in range(m)]
temp2_set = set()
for i in range(n):
    temp2_field[0][i] = True
    temp2_set.add((0,i))
for i in range(m):
    temp2_field[i][n-1] = True 
    temp2_set.add(((i,n-1)))

for i in range(1,n):
    temp2_field[1][i] = True
    temp2_set.add((1,i))
for i in range(1,m-1):
    temp2_field[i][m-2] = True
    temp2_set.add((i,m-2))


'''
Creates dictionary that holds the nodes and connections
Keys: Nodes
Values: Nodes that are connected to each key node
Parameters: The dictionary you want to fill
'''
def create_dic(dic):
    for x in range(m):
        for y in range(n):
            if(x == 0):
                if(y == 0):
                    dic[(x,y)] = [(x,y+1), (x+1,y)]
                elif(y == n-1):
                    dic[(x,y)] = [(x+1,y), (x,y-1)]
                else:
                    dic[(x,y)] = [(x,y+1), (x+1,y), (x,y-1)]
            elif(x != m-1):
                if(y == 0):
                    dic[(x,y)] = [(x,y+1), (x+1,y), (x-1,y)]
                elif(y == n-1):
                    dic[(x,y)] = [(x+1,y), (x,y-1), (x-1,y)]
                else:
                    dic[(x,y)] = [(x,y+1), (x+1,y), (x,y-1), (x-1,y)]
            else:
                if(y == 0):
                    dic[(x,y)] = [(x,y+1), (x-1,y)]
                elif(y == n-1):
                    dic[(x,y)] = [(x,y-1), (x-1,y)]
                else:
                    dic[(x,y)] = [(x,y+1), (x,y-1), (x-1,y)]
    return dic


'''
Prints field for visualization
Parameters: field you want to visualize
'''
def print_field(field):
    for i,x in enumerate(field):
        for j,y in enumerate(x):
            if y:
                print('[X]',end=' ')
            else:
                print('[O]',end=' ')
        print()
    print()
    time.sleep(0.3) #Delay to see field change


#Parameters: Graph to be used, starting node, set of visited nodes, field to print
def dfs(graph, node, visited, field):
    global battery
    #If the current node has been visited just return the current set
    if node in visited:
        return visited
    
    #If the battery is below safty limit, end DFS by returning False
    if battery <= LIMIT:
        print("Limit!")
        return visited
    
    battery -= sq_cost #Drains battery per node visited
    print('Current neighbor nodes: {}'.format(graph[node]))
    visited.add(node) #Adds node to set
    field[node[0]][node[1]] = True #Sets the node in the printed field to True so it can be visialized as visited
    print_field(field) #Print the current field after visiting the node

    #Recursivly calls the function to search all connected nodes 
    for neighbor in graph[node]:
        if neighbor not in visited:
            result = dfs(graph, neighbor, visited, field)
            # If the limit is reached in a recursive call, return immediately
            if battery <= LIMIT:
                return result

    return visited

# Runs test on certain field based on paramter 'f' input
def test(f):
    g = create_dic(graph)
    if f == 1:
        print_field(field)
        visited = dfs(g,(0,0), set(), field)
    elif f == 2:
        print_field(temp_field)
        visited = dfs(g,(m-1,n-2), temp_set, temp_field)
    elif f == 3:
        print_field(temp2_field)
        visited = dfs(g,(1,0), temp2_set, temp2_field)
    
    print('Set of visited nodes: \n{}'.format(visited))


def main():
    test(1)

if __name__=="__main__":
    main()