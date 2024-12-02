# Graph has x axis pointing down and y axis is pointing right
graph = {(0,0): [(1,0),(0,1)]} #dictonary containing all verticies and edges

m, n = 20, 20

def print_field():
    for x in range(m):
        for y in range(n):
            print('({},{})'.format(x,y),end=' ')
        print()

for x in range(m):
    for y in range(n):
        if(x == 0):
            if(y == 0):
                graph[(x,y)] = [(x,y+1), (x+1,y)]
            elif(y == n-1):
                graph[(x,y)] = [(x+1,y), (x,y-1)]
            else:
                graph[(x,y)] = [(x,y+1), (x+1,y), (x,y-1)]
        elif(x != m-1):
            if(y == 0):
                graph[(x,y)] = [(x,y+1), (x+1,y), (x-1,y)]
            elif(y == n-1):
                graph[(x,y)] = [(x+1,y), (x,y-1), (x-1,y)]
            else:
                graph[(x,y)] = [(x,y+1), (x+1,y), (x,y-1), (x-1,y)]
        else:
            if(y == 0):
                graph[(x,y)] = [(x,y+1), (x-1,y)]
            elif(y == n-1):
                graph[(x,y)] = [(x,y-1), (x-1,y)]
            else:
                graph[(x,y)] = [(x,y+1), (x,y-1), (x-1,y)]
        

print_field()

for key, values in graph.items():
    print('{}: {}'.format(key, values))