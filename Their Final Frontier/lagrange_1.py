class Lagrange:
    
    #initiate map
    data_points = {}
    
    def __init__(self, x_val, y_val, size):
        self.x_val = x_val
        self.y_val = y_val
        self.size = size
             
        #Stores the x values in a hash map 
        for x, y in zip(self.x_val, self.y_val):
            self.data_points[x] = y
            

    #Use another arg name for X as x is used for other things. 
    def lagrange(self, target_x, n):
        
        if n > self.size:
            n = self.size
            
        lagrange_val = 0    
        
        #if n is odd~
        if n%2!=0:  
            counter = 0
            for i in range(len(self.x_val)):
                if target_x > self.x_val[i]:
                    counter += 1
                else:
                    continue
            if counter <= (n // 2):
                points_nearest = sorted(self.x_val, key=lambda x: abs(x - target_x))[:n]  
            else:
                points_nearest = sorted(self.x_val, key=lambda x: abs(x - target_x))[:n-1]     
                points_nearest.insert(0, self.x_val[self.x_val.index(sorted(points_nearest)[0])-1])  
        else:
            points_nearest = sorted(self.x_val, key=lambda x: abs(x - target_x))[:n]  
        
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