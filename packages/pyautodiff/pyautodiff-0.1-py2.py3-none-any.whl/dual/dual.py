import numpy as np

class Dual:
    """ 
    This is a class for mathematical operations on dual numbers. 
      
    Attributes: 
        val (float): function value of dual number. 
        der (float): derivative part of dual number. 
    """
    
    def __init__(self, x, der=1):
        """ 
        The constructor for Dual class. 
  
        Parameters: 
            val (float): function value of dual number. 
            der (float): derivative part of dual number.   
        """
        self.val = x
        self.der = der
        
    ## UNARY OPERATIONS
        
        
    def __neg__(self):
        """ 
        The function for unitary negative operation. 
  
        Parameters: 
            self (Dual): The dual number to perform the unitary negative operation. 
          
        Returns: 
            Dual: A dual number which contains the result. 
        """
        return Dual(-self.val, -self.der)
    
    
    def __pos__(self):
        """ 
        The function for unitary plus operation. 
  
        Parameters: 
            self (Dual): The dual number to perform the unitary plus operation. 
          
        Returns: 
            Dual: A dual number which contains the result. 
        """
        return Dual(+self.val, +self.der)
        
        
    ## PLUS OPERATIONS
    
    def __add__(self, other):
        """ 
        The function to add two dual number or a dual number from the left. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (Dual / float): The dual/float number to be added.
          
        Returns: 
            Dual: A dual number which contains the sum. 
        """
        try:
            return Dual(self.val + other.val, self.der + other.der)
        except AttributeError:
            return Dual(self.val + other, self.der)
    
    def __radd__(self, other):
        """ 
        The function to add a dual number from the right. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (float): The float number to be added.
          
        Returns: 
            Dual: A dual number which contains the sum. 
        """
        return Dual(other + self.val, self.der)
    
    
    ## MINUS OPERATIONS
    
    def __sub__(self, other):
        """ 
        The function to substract two dual number or a dual number from the left. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (Dual / float): The dual/float number to be substracted.
          
        Returns: 
            Dual: A dual number which contains the difference. 
        """
        try:
            return Dual(self.val - other.val, self.der - other.der)
        except AttributeError:
            return Dual(self.val - other, self.der)
        
    def __rsub__(self, other):
        """ 
        The function to substract a dual number from a float number. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (float): The float number to be substracted from.
          
        Returns: 
            Dual: A dual number which contains the difference. 
        """
        return Dual(other - self.val, -self.der)
        
    
    ## MULTIPLICATION OPERATIONS
    
    def __mul__(self, other):
        """ 
        The function to multiply two dual number and to multiply a dual number from the left. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (Dual / float): The dual/float number for multiplication.
          
        Returns: 
            Dual: A dual number which contains the product. 
        """
        try:
            # multiplication rule
            temp = self.val * other.der + self.der * other.val
            return Dual(self.val * other.val, temp)
        except AttributeError:
            return Dual(self.val * other, self.der * other)

    def __rmul__(self, other):
        """ 
        The function to multiply a dual number from the right. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (float): The float number for multiplication.
          
        Returns: 
            Dual: A dual number which contains the product. 
        """
        return Dual(self.val * other, self.der * other)
    
    
    ## DIVISION OPERATIONS
        
    def __truediv__(self, other):
        """ 
        The function to divide two dual number and to divide a dual number by a float number. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (Dual / float): The dual/float number for division.
          
        Returns: 
            Dual: A dual number which contains the quotient. 
        """
        try:
            # quotient rule
            temp = (self.der * other.val - self.val * other.der)
            print(self.der)
            print(other.der)
            return Dual(self.val/other.val, temp/other.val ** 2)
        except AttributeError:
            # divide by a constant
            return Dual(self.val/other, self.der/other)
        
    def __rtruediv__(self, other):
            """ 
            The function to divide a float by a dual number. 
  
            Parameters: 
                self (Dual): The current dual number.
                other (float): The float number for division.
          
            Returns: 
                Dual: A dual number which contains the quotient. 
            """
            return Dual(other/self.val, -other/self.val**2*self.der)   
    
    
    ## POWER OPERATIONS
    
    def __pow__(self, other):
        """ 
        The function to exponentiate a dual number by a float or dual number. 
  
        Parameters: 
            self (Dual): The current dual number.
            other (Dual / float): The dual/float number for exponentiation.
          
        Returns: 
            Dual: A dual number which contains the power. 
        """
        try:
            # da^u/dx = ln(a) a^u du/dx
            factor = self.val ** (other.val -1)
            sum_1 = other.val * self.der
            sum_2 = self.val * np.log(self.val) * other.der
            temp = factor * (sum_1 + sum_2)
            return Dual(self.val ** other.val, temp)
        except AttributeError:
            # du^n/dx = n * u^(n-1) * du/dx
            temp = other * self.val ** (other-1) * self.der
            return Dual(self.val ** other, temp)
        
    def __rpow__(self, other):
            """ 
            The function to exponentiate a float number by a dual number. 
  
            Parameters: 
                self (Dual): The current dual number.
                other (float): The float number for exponentiation.
          
            Returns: 
                Dual: A dual number which contains the power. 
            """
            # da^u/dx = ln(a) a^u du/dx
            temp = np.log(other) * other ** self.val * self.der
            return Dual(other ** self.val, temp)
        