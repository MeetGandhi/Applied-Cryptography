from time import time
t=time()
def EuclideanGCD(a,b):
    if a==0:
        return (b,0,1)
    else:
        g,y,x=EuclideanGCD(b%a,a)
        return(g,x-(b//a)*y,y)
def modinverse(a,m):
    g,x,y=EuclideanGCD(a,m)
    if g!=1:
        print("Modular inverse does not exist.")
    else:
        return x%m
#print "Time Taken: "+str(time()-t)+" seconds."
k=input("Enter k:")
N=input("Enter N:")
M=modinverse(k,N)
print("Modular inverse of "+str(k)+" mod "+str(N)+" is "+str(M)+" mod "+str(N)+".")
