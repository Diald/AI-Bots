import numpy as np 

a = np.array([1,2,3])
#print(a)

b = np.array([[1,2,3,4],[5,6,7,8]]) #2D array / matrix 
#print(b)

#arrays with zeroes or ones 
zeroes = np.zeros((2,3)) # array of size (2,3)
ones = np.ones((2,3)) #array of size(2,3) having only ones

#print(zeroes)
#print(ones)

#RANGE OF NUMBERS 
c = np.arange(0,10,2)
d = np.linspace(0,1, 5)


print(b.shape) #(2,4) which is 2 rows and 4 columns
print(b.ndim) # dimensions which is 2
print(b.size) #total number of elements which is 8 [2*4]
print(b.dtype) #the data type which is int32


#INDEXING AND SLICING 
print(b[0,1]) #the element at 0th row and 1st column or b[0][1]
print(b[:,1]) # the entire second column or 1st column 
print(b[1,:]) # the entire second row or 1st row 
print(b[0:2, 1:3]) # subarray from 0th


#MATHEMATICAL OPERATIONS 
x = np.array([1,2,3])
y = np.array([4,5,6])

print(x+y) #[5 7 9]
print(x-y) #[-3 -3 -3]
print(x*y) # [4 10 18]
print(x/y) # [0.25 0.4 0.5]

print(np.sqrt(x))
print(np.exp(x)) # e ki power x[i]


#MATRIX OPERATIONS - 

a = np.array([[1,2], [3,4]])
b = np.array([[2,0],[1,3]])

#matrix multiplication 
print(a@b) 
print(np.dot(a, b))

print(np.linalg.inv(a)) # inverse of A 
print(np.linalg.det(a)) # determinant of A 
print(np.linalg.eig(a)) # eigen values and eigen vectors


#AGGREGATIONS - Statistics 

arr = np.array([1,2,3,4,5])
print(arr.sum())
print(arr.mean())
print(arr.min())
print(arr.max())
print(arr.std())