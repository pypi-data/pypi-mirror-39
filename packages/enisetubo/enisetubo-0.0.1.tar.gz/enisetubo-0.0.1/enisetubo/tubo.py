from random import normalvariate, triangular

def boule(p,d,mat):
    prod={}
    if mat == 'acier':
        prod['poids']    = normalvariate(p, .020*p)
        prod['diametre'] = normalvariate(d, .018*d)
    if mat == 'fonte':
        prod['poids']    = triangular(p-10, p+10)        
        prod['diametre'] = triangular(d-5,d+5)
    prod['materiau']=mat
    return prod