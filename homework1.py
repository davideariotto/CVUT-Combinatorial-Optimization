import itertools
from recordclass import recordclass
from collections import deque
import heapq
import time



# C = capacity
# MC = minimum cost
# items = list of tuples: each tuple represents weight and cost of an item

def bruteForceIteration(C, MC, items):
    
    bestSolution = []
    bestValue = 0
    bestWeight = 0
    for l in range(0, len(items)+1):
        for subset in itertools.combinations(items, l):
            
            sumValue = 0
            sumWeight = 0
            
            for i in subset:
                sumWeight = sumWeight+i[0]
                sumValue = sumValue+i[1]
                
            if sumWeight <= C and sumValue > bestValue and sumValue > MC:
                bestValue = sumValue
                bestWeight = sumWeight
                bestSolution = subset
    print ("The best solution is " + str(bestSolution) + " with a weight of " + str(bestWeight) + " and value of " + str(bestValue))

# num = number of recursion call
def bruteForceRecursion(C, wt, val, n, listR):
    
    listR.append(0)
    
    if n == 0 or C == 0:
        return 0
 
    # we can't go deeper
    if (wt[n-1] > C):
        return bruteForceRecursion(C, wt, val, n-1, listR)
 
    # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(val[n-1] + bruteForceRecursion(C-wt[n-1], wt, val, n-1, listR), bruteForceRecursion(C, wt, val, n-1, listR))
    
    
    
    
# Start of branch&bound part

Item = recordclass('Item', 'index value weight')
Node = recordclass('Node', 'level value weight items')
PQNode = recordclass('PQNode', 'level value weight bound items')

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
    def empty(self):
        if (len(self._queue) == 0):
            return True
        else:
            return False

    def length(self):
        return len(self._queue)
    

def branch_bound_breadth_first(it, capacity, item_count, numR):
    
    items = []

    for i in range(0, item_count):  
        items.append(Item(i, int(it[i][1]), int(it[i][0])))

    items = sorted(items,key=lambda Item: Item.weight/Item.value)    
    
    v = Node(level = -1, value = 0, weight = 0, items = [])
    Q = deque([])
    Q.append(v)
    
    maxValue = 0    
    bestItems = []
    
    while (len(Q) != 0):
        
        # Increase recursion number for the statistic
        numR = numR + 1
        
        
        v = Q[0]

        Q.popleft()
        
        u = Node(level = None, weight = None, value = None, items = [])
        
        u.level = v.level + 1
        u.weight = v.weight + items[u.level].weight
        u.value = v.value + items[u.level].value
        u.items = list(v.items)       
        u.items.append(items[u.level].index)
        
        if (u.weight <= capacity and u.value > maxValue):
            maxValue = u.value
            bestItems = u.items
        
        bound_u = bound(u, capacity, item_count, items)
                
        if (bound_u > maxValue):
            Q.append(u)
                
        u = Node(level = None, weight = None, value = None, items = [])
        u.level = v.level + 1
        u.weight = v.weight
        u.value = v.value
        u.items = list(v.items)
      
        bound_u = bound(u, capacity, item_count, items)

        if (bound_u > maxValue):
            Q.append(u)
    
    taken = [0]*len(items)    
    for i in range(len(bestItems)):
        taken[bestItems[i]] = 1
    output_data = str(maxValue) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    print(output_data)
    return numR

     
def bound(u, capacity, item_count, items):
    if (u.weight >= capacity):
        return 0
    else:
        result = u.value
        j = u.level + 1
        totweight = u.weight
        
        while (j < item_count and totweight + items[j].weight <= capacity):
            totweight = totweight + items[j].weight
            result = result + items[j].value
            j = j + 1
        
        k = j
        if (k <= item_count - 1):
            result = result + (capacity - totweight)*items[k].value/items[k].weight
        
        return result
        



def main():
    
    # importing data
    with open('NR/NR10_inst.dat') as f:
        lines = f.readlines()
    
    numR = []
    
    #map for histogram
    #mapB = {400:0, 800:0,1200:0,1600:0,2000:0}
    mapB = {40:0, 80:0,120:0,160:0,200:0}
    
    # Number of instances for a clearer print
    countLines = 0
    
    for line in lines:
        
        countLines = countLines+1
        
        # for every line I solve the knapsack problem
        data = line.split()
        
        # number of items
        num = int(data[1])
        
        # capacity of knapsack
        capacity = int(data[2])
        
        #minimum cost
        minCost = int(data[3])  
        
        #number of recursion
        listR = []
        
        # available items
        items = []
        wt = []
        val = []
        
        for i in range(4, 3+(num*2) ,2):
            items.append((int(data[i]), int(data[i+1])))
            wt.append(int(data[i]))
            val.append(int(data[i+1]))
                  
        print("Solution of instance n°" + str(countLines))
        # bruteForceIteration(capacity, minCost, items)
        
        # Brute force recursion:
        
        #st = time.process_time()
        #print("Value: " + str(bruteForceRecursion(capacity, wt, val, len(items), listR)))
        #et = time.process_time()
        #numR.append( len(listR) )
        
        #rest = int( len(listR) / 400 )
        #if rest == 0:
            #mapB[400] = mapB.get(400) + 1
        #elif rest == 1:
            #mapB[800] = mapB.get(800) + 1
        #elif rest == 2:
            #mapB[1200] = mapB.get(1200) + 1
        #elif rest == 3:
            #mapB[1600] = mapB.get(1600) + 1
        #elif rest == 4:
            #mapB[2000] = mapB.get(2000) + 1
            
        #print(rest)
        
        
        
        # Branch & Bound:
        
        st = time.process_time()
        res = branch_bound_breadth_first(items, capacity, len(items), 0)
        et = time.process_time()
        numR.append(res)
        
        rest = int( res / 40 )
        if rest == 0:
            mapB[40] = mapB.get(40) + 1
        elif rest == 1:
            mapB[80] = mapB.get(80) + 1
        elif rest == 2:
            mapB[120] = mapB.get(120) + 1
        elif rest == 3:
            mapB[160] = mapB.get(160) + 1
        elif rest == 4:
            mapB[200] = mapB.get(200) + 1
        
        print("")
    
    print("Total number of recursion calls: " + str(sum(numR)))
    print("Maximum number of recursion calls: " + str(max(numR)))
    print("Average number of recursion calls: " + str(sum(numR)/len(numR)))
    print("CPU time: " + str(et - st) + " seconds")
    print()
    print(mapB)
    
        
        

main()

