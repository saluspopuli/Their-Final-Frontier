class Lagrange:
    
    #initiate map
    data_points = {}
    
    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val
             
        #Stores the x values in a hash map 
        for x, y in zip(self.x_val, self.y_val):
            self.data_points[x] = y
            

    #Use another arg name for X as x is used for other things. 
    def lagrange(self, target_x, n=100):
        
        if n > len(self.x_val):
            n = len(self.x_val)
            
        lagrange_val = 0 
        
        # Sort the x values based on the absolute difference from the target_x
        sorted_x_val = sorted(self.x_val, key=lambda x: abs(x - target_x))
        # Stores the first n values to the points nearest.
        points_nearest = sorted_x_val[:n]  
        
        #This is a pretty slow algo, can be better but placeholder for now. 
        for i in range(n):
            #Getting Li
            li_var = 1 
            for j in range(n):  
                if j != i:   
                    updated_li_var = (target_x - points_nearest[j])/(points_nearest[i] - points_nearest[j])
                    li_var *= updated_li_var
                else:
                    continue
            #Getting Lagrange. f(x) = Li(x)f(Xi) where f(X) = target_y.
            target_y = (li_var) * (self.data_points.get(points_nearest[i], None))
            lagrange_val += target_y
            
        return lagrange_val

    def add_point(self, x, y):
        
        self.data_points = {}
        
        self.x_val.append(x)
        self.y_val.append(y)
        
        #Stores the x values in a hash map 
        for x, y in zip(self.x_val, self.y_val):
            self.data_points[x] = y