from recordclass import recordclass
from collections import deque
import heapq
import time

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
    

def branch_bound_breadth_first(it, capacity, item_count):
    
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
    return

     
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
        
# Simple heuristic
def simpleHeuristic(it, capacity, item_count, solution):
    i = 0
    sortedItems = sorted(it, key=lambda x: (x[1]/x[0]), reverse=True)
    currentCost = 0
    currentWeight = 0
    newItems = []
    
    n = item_count
    for si in sortedItems:
        if(si[0] <= capacity):
            newItems.append(si)
        else:
            n -= 1
    
    for i in range(n):
        if currentWeight+newItems[i][0] > capacity:
            break
        currentCost += newItems[i][1]
        currentWeight += newItems[i][0]   
    
    if(solution==0):
        res = currentCost
        print(""+str(round(res*100, 2)) + " %")
        return currentCost
    res =  ((solution-currentCost)/solution)
    print(""+str(round(res*100, 2)) + " %")
    return res

# Extended heuristic
def extendedHeuristic(it, capacity, item_count, solution):
    i = 0
    sortedItems = sorted(it, key=lambda x: (x[1]/x[0]), reverse=True)
    currentCost = 0
    currentWeight = 0
    
    newItems = []
    
    n = item_count
    for si in sortedItems:
        if(si[0] <= capacity):
            newItems.append(si)
        else:
            n -= 1
    
    for i in range(n):
        if currentWeight+newItems[i][0] > capacity:
            break
        currentCost += newItems[i][1]
        currentWeight += newItems[i][0]  
      
    if(len(newItems) != 0):
        mostExpensiveNewItems = sorted(newItems, key=lambda x: (x[1]), reverse=True) 
        mostExpensiveItem = mostExpensiveNewItems[0]
        
    res = 0
    if(solution==0):
        res = currentCost
        print(""+str(round(res*100, 2)) + " %")
        return res
    else:
        res = min(((solution-currentCost)/solution), ((solution-mostExpensiveItem[1])/solution))
        print(""+str(round(res*100, 2)) + " %")
        return res
        
            

# Recursive Dynamic programming
def dynamicProgramming(capacity, weights, costs, numI):
    K = [[0 for x in range(capacity + 1)] for x in range(numI + 1)]
 
    # Build table K[][] in bottom up manner
    for i in range(numI + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i-1] <= w:
                K[i][w] = max(costs[i-1] + K[i-1][w-weights[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
 
    return K[numI][capacity]

# Modified recursive dynamic programming that computes the error (for FPTAS)
def modDynamicProgramming(capacity, weights, costs, numI, solution, scalingFactor):
    K = [[0 for x in range(capacity + 1)] for x in range(numI + 1)]
 
    # Build table K[][] in bottom up manner
    for i in range(numI + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i-1] <= w:
                K[i][w] = max(costs[i-1] + K[i-1][w-weights[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    
    if(solution==0):
        res = (K[numI][capacity] * scalingFactor)
        print(""+str(round(res*100, 2)) + " %")
        return res
    
    # compute error
    res = (solution - (K[numI][capacity] * scalingFactor))/solution
    print(""+str(round(res*100, 2)) + " %")
    return res

# FPTAS approximation algorithm
def FPTAS(capacity, weights, costs, numI, solution, epsilon=0.1):
    
    n = numI
    for w in weights:
        if(w > capacity):
            costs.pop(weights.index(w))
            weights.remove(w)
            n -= 1
    
    maxCost = max(costs)
    K = epsilon * maxCost / numI
    
    newCosts = [(int(c / K)) for c in costs]
    return modDynamicProgramming(capacity, weights, newCosts, n, solution, K)

# Iterative dynamic prpogramming
def iterativeDynamicProgramming(capacity, weights, costs, numI):
    
    n = numI
    for w in weights:
        if(w > capacity):
            costs.pop(weights.index(w))
            weights.remove(w)
            n -= 1
    
    costTable = [ [ 0 for i in range(capacity+1) ] for j in range(n+1) ]
    
    for i in range(1,n):
        for w in range(capacity+1):
              
            if weights[i] <= w:
                costTable[i][w] = max(costs[i] + costTable[i-1][w - weights[i]], costTable[i-1][w])
            else:
                costTable[i][w] = costTable[i-1][w]
                

    return costTable[n-1][capacity]
        

def main():
    
    # importing data
    with open('ZKW/ZKW30_inst.dat') as f:
        lines = f.readlines()
    
    #importing solution
    with open('ZKW/ZKW30_sol.dat') as f2:
        lines2 = f2.readlines()
    
    solList = []
    solDict = {}
    
    for l in lines2:
        d = l.split()
        solDict[d[0]] = int(d[2])
    
    
    errorList = []
    
    
    for line in lines:
        
        # for every line I solve the knapsack problem
        data = line.split()
        
        # id of the instance
        idR = data[0]
        
        # number of items
        num = int(data[1])
        
        # capacity of knapsack
        capacity = int(data[2])
        
        # available items
        items = []
        wt = []
        val = []
        
        for i in range(3, 3+(num*2) ,2):
            items.append((int(data[i]), int(data[i+1])))
            wt.append(int(data[i]))
            val.append(int(data[i+1]))
                  
        print("Solution of instance n°" + idR)
        
        # Branch & Bound:
        #st = time.time()
        #st = time.time_ns()
        #branch_bound_breadth_first(items, capacity, len(items))
        #et = time.time_ns()
        #et = time.time()
        
        # Simple/Extended Heuristic:
        #st = time.time()
        st = time.time_ns()
        #errorList.append(simpleHeuristic(items, capacity, len(items), solDict[idR]))
        errorList.append((extendedHeuristic(items, capacity, len(items), solDict[idR])))
        et = time.time_ns()
        #et = time.time()
        
        # Dynamic programming and FPTAS
        #st = time.time()
        #st = time.time_ns()
        #print(dynamicProgramming(capacity, wt, val, num))
        #errorList.append((FPTAS(capacity, wt, val, num, solDict[idR])))
        #print(iterativeDynamicProgramming(capacity, wt, val, num))
        #et = time.time_ns()
        #et = time.time()
        
        print("")
        
        
    
    #print("Runtime: " + str(round((et - st)*1000,4)) + " milliseconds")
    print("Runtime: " + str(round((et - st)/1000,4)) + " microseconds")
    # Comment below for branch&bound and dynamic programming
    print("Average error: " + str(round(sum(errorList)*100/len(errorList),2)) + " %")
    print("Maximum error: " + str(round(max(errorList)*100,2)) + " %")
    
    

main()
