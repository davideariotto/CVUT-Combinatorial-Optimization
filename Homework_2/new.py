
def newDyn(capacity, weights, costs, numI):
    
    maxPrice = sum(costs)
    K = [[0 for x in range(numI + 2)] for x in range(maxPrice + 2)]
            
    for item in range(numI+1):
        for price in range(maxPrice+1):
            if price == 0:
                continue
            if item == 0:
                K[price][item] = 1000000
                continue
                    
            if item == 1:
                if price == costs[item-1]:
                    K[price][item] = weights[item-1]
                else:
                    K[price][item] = 1000000  
                continue
            
            lastWeight = K[price][item-1]
            priceIndex = price - costs[item-1]
            
            if priceIndex < 0:
                if lastWeight == 1000000:
                    K[price][item] = 1000000
                else:
                    K[price][item] = lastWeight
            else:
                if K[priceIndex][item-1] == 1000000:
                    K[price][item] = min(lastWeight, K[priceIndex][item-1])
                else:
                    K[price][item] = min(lastWeight, K[priceIndex][item-1]+weights[item-1])
            
              
            res = 0      
            for rowIndex in range(maxPrice-1, 0, -1):
                if K[rowIndex][item-1] <= capacity:
                    res = K[rowIndex][item]
                    #res = rowIndex
                    break
             
            return res   