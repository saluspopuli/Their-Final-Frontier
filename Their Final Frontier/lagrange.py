class Lagrange:
    
    def __init__(self, coordinates = [(0,0)]):
        self.coordinates = coordinates
        # Sorts the coordinates with respect to the x value
        self.coordinates = sorted(self.coordinates, key=lambda coord: coord[0])
        # Updates the list of indices for the coordinates list
        self.indices = list(range(len(self.coordinates)))

    #Use another arg name for X as x is used for other things. 
    def lagrange(self, target_x, n): 
        
        lagrange_val = 0
        
        # Ensures that n will never go beyond the amount of coordinates currently loaded
        if n > len(self.coordinates):
            n = len(self.coordinates)
        
        # Gets the index of the data point that is right after the target_x
        root_index = len(self.coordinates)-1
        for i, coord in enumerate(self.coordinates):
            if coord[0] > target_x: 
                root_index = i
                break
        
        # Sorts the indices by which is closest to the root_index
        sorted_indices = sorted(self.indices, key=lambda idx: abs(idx - root_index))
        
        # TODO: @Jamille, documment this part of your code ok thx
        for i in range(n):
            # Getting Li
            li_var = 1 
            for j in range(n):  
                if j != i:   
                    li_var *= (target_x - self.coordinates[sorted_indices[j]][0]) / (self.coordinates[sorted_indices[i]][0] - self.coordinates[sorted_indices[j]][0])
            
            # Getting Lagrange. f(x) = Li(x)f(Xi) where f(X) = target_y.
            target_y = li_var * self.coordinates[sorted_indices[i]][1]
            lagrange_val += target_y
            
        return lagrange_val
    

    # Adds a data point 
    def add_point(self, x, y):
        # Check if the new (x, y) values already exist in the coordinates list
        if (x, y) not in self.coordinates:  
            # Adds new x and y values to the coordinates list
            self.coordinates.append((x, y))
            # Sorts the coordinates with respect to the x value
            self.coordinates = sorted(self.coordinates, key=lambda coord: coord[0])
            # Updates the list of indices for the coordinates list
            self.indices = list(range(len(self.coordinates)))