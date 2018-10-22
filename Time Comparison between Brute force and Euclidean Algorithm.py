from time import time
def bruteForceGCD(a,b):
  g=1
  d=1
  while(d*d<=b):
    if (b%d==0):
        if (a%d==0):
            g=max(g,d)
        if (a%(b/d)==0):
            g=max(g,b/d)
    d=d+1
  print g
  print "Time Taken by Brute Force Algorithm: "+str(time()-t)+" seconds."
def EuclideanGCD(a,b):
  if a==0:
      return (b,0,1)
  else:
      g,y,x=EuclideanGCD(b%a,a)
      return(g,x-(b//a)*y,y)
    
    
b=input("Enter the smaller number:")
a=input("Enter the larger number:")
t=time()
bruteForceGCD(a,b)
T=time()
g,y,x=EuclideanGCD(a,b)
print g
E=time()-T
print "Time Taken by Euclidean Algorithm: "+str(E)+" seconds."
