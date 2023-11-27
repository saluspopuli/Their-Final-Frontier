import random #TODO: GET RID OF THIS

class Lagrange:
    
    indices = []
    
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.coordinates = sorted(self.coordinates, key=lambda coord: coord[0])
        self.indices = list(range(len(self.coordinates)))

    #Use another arg name for X as x is used for other things. 
    def lagrange(self, target_x, n): 
        
        lagrange_val = 0
        
        if n > len(self.coordinates):
            n = len(self.coordinates)
        
        root_index = len(self.coordinates)-1
        for i, coord in enumerate(self.coordinates):
            if coord[0] > target_x: 
                root_index = i
                break
        
        sorted_indices = sorted(self.indices, key=lambda idx: abs(idx - root_index))
        for i in range(n):
            # Getting Li
            li_var = 1 
            for j in range(n):  
                if j != i:   
                    updated_li_var = (target_x - self.coordinates[sorted_indices[j]][0]) / (self.coordinates[sorted_indices[i]][0] - self.coordinates[sorted_indices[j]][0])
                    li_var *= updated_li_var
            
            # Getting Lagrange. f(x) = Li(x)f(Xi) where f(X) = target_y.
            target_y = li_var * self.coordinates[sorted_indices[i]][1]
            lagrange_val += target_y
            
        return lagrange_val
    

    def add_point(self, x, y):
        
        self.coordinates.append((x,y))
        self.coordinates = sorted(self.coordinates, key=lambda coord: coord[0])
        self.indices = list(range(len(self.coordinates)))