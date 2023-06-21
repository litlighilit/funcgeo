
def rmtan90(exp,y,x,*,abs_tol=0.1):
    ntan=exp.find('tan(')
    if ntan!=-1:
        intan=set()
        def findintan(s,n):
            n0=n=n+4
            nn=1
            while all([n<len(s),nn!=0]):
                ss=s[n]
                if ss=='(':nn+=1
                elif ss==')':nn-=1
                n+=1
            nns=s[n0:n-1]
            intan.add(nns)
            n1=nns.find('tan(')
            if n1!=-1:findintan(nns,n1)
        findintan(exp,ntan)
        from numpy import cos,nan
        for e in intan:
            y[abs(cos(eval(e)))<=abs_tol]=nan
        del intan
        
if __name__=='__main__':
    from numpy import linspace,tan,pi
    
    x=linspace(0,pi,3)
    print(x)
    s='tan(x)'
    y=eval(s)
    print(y)
    rmtan90(s,x,y)
    print(y)
