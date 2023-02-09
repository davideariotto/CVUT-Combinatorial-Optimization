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


def bruteForceRecursion(C, wt, val, n, listR):
    
    # The length of this list will be equal to the number of recursion calls
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
    

def main():
    
    # importing data
    with open('data.txt') as f:
        lines = f.readlines()
    
    #importing solution
    solList = []
    solDict = {}
    
    #calculate solution
    for l in lines:
        data = l.split()
        idR = data[0]
        num = int(data[1])
        capacity = int(data[2])
        items = []
        wt = []
        val = []
        
        for i in range(3, 3+(num*2) ,2):
            items.append((int(data[i]), int(data[i+1])))
            wt.append(int(data[i]))
            val.append(int(data[i+1]))
                  
        solDict[data[0]] = dynamicProgramming(capacity, wt, val, num)
    
    
    errorList = []
    listR = []
    resR = []
    count = 0
    
    
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
        
        # Brute Force:
        #st = time.time()
        st = time.time_ns()
        #listR.clear()
        print(bruteForceRecursion(capacity, wt, val, num, listR))
        #resR.append(len(listR))
        et = time.time_ns()
        #et = time.time()
        
        # Branch & Bound:
        #st = time.time()
        #st = time.time_ns()
        #branch_bound_breadth_first(items, capacity, len(items))
        #et = time.time_ns()
        #et = time.time()
        
        # Simple Heuristic:
        #st = time.time()
        #st = time.time_ns()
        #errorList.append(simpleHeuristic(items, capacity, len(items), solDict[idR]))
        #et = time.time_ns()
        #et = time.time()
        
        # Dynamic programming 
        #st = time.time()
        #st = time.time_ns()
        #print(dynamicProgramming(capacity, wt, val, num))
        #et = time.time_ns()
        #et = time.time()
        
        print("")
        
        
    
    #print("Runtime: " + str(round((et - st)*1000,4)) + " milliseconds")
    print("Runtime: " + str(round((et - st)/1000,4)) + " microseconds")
    #print("Average number of recursion calls: ", str(round(sum(resR)/len(resR),2)))
    # Comment below for branch&bound, dynamic programming and brute force
    #print("Average error: " + str(round(sum(errorList)*100/len(errorList),2)) + " %")
    #print("Maximum error: " + str(round(max(errorList)*100,2)) + " %")
    

def perm():
      
      # importing data
    with open('permData.txt') as f:
        lines = f.readlines()
        
    #importing solution
    solList = []
    solDict = {}
    
    #calculate solution
    count = 1
    for l in lines:
        data = l.split()
        idR = data[0]
        num = int(data[1])
        capacity = int(data[2])
        items = []
        wt = []
        val = []
        
        for i in range(3, 3+(num*2) ,2):
            items.append((int(data[i]), int(data[i+1])))
            wt.append(int(data[i]))
            val.append(int(data[i+1]))
                  
        solDict[str(data[0])+"_"+str(count)] = dynamicProgramming(capacity, wt, val, num)
        count+=1
        if(count==4):
            count=1
    
    errorList = []
    listR = []
    resR = []
    count = 1
    
    
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
                  
        if(count==1):
            print("Solution of instance n°" + idR)
        
        # Brute Force:
        #st = time.time()
        #st = time.time_ns()
        #listR.clear()
        #bruteForceRecursion(capacity, wt, val, num, listR)
        #resR.append(len(listR))
        #et = time.time_ns()
        #et = time.time()
        
        # Branch & Bound:
        #st = time.time()
        #st = time.time_ns()
        #branch_bound_breadth_first(items, capacity, len(items))
        #et = time.time_ns()
        #et = time.time()
        
        # Simple Heuristic:
        #st = time.time()
        st = time.time_ns()
        errorList.append(simpleHeuristic(items, capacity, len(items), solDict[str(idR)+"_"+str(count)]))
        et = time.time_ns()
        #et = time.time()
        
        # Dynamic programming 
        #st = time.time()
        #st = time.time_ns()
        #dynamicProgramming(capacity, wt, val, num)
        #et = time.time_ns()
        #et = time.time()
        
        print("Runtime of permutation n° "+ str(count) + " : " + str(round((et - st)/1000,4)) + " microseconds")
        count+=1
        if(count==4):
            count = 1
        print("")
        
        
    

#main()

perm()
