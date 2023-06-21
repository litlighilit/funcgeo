from numpy import *
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus']=False

from .tools.rmtan90 import rmtan90
from .tools.replace import *


def get_mode():
    global m0
    m1=list('bcgkmrwy')
    m2='-- - -. :'.split()
    m3=list('.,ov^<>1234sp*hHd|_+x')
    for i in m1,m2,m3:
        i.append('')
    m0=[]
    for i in m1:
        for j in m2:
            for z in m3:
                m0.append(i+j+z)

def gets(st):
    global s, ls, le,n,mode,sf
    #ss = input("func expression(press Enter to plot):")
    s=st if not st.isspace() else '(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0' 
    if s == ('quit()' or 'exit()'): exec(s)
    ls = s.lower().split(',')
    on,om=True,True
    i = 0
    while i <=len(ls)-1:
        if 'n=' in ls[i]:
            n=eval(ls.pop(i).replace('n=',''))
            on=False
            i-=1
        if ls[i] in m0:
            mode=ls.pop(i)
            om=False
            i-=1
        i+=1
    if on:n=100
    if om:mode='b-'
    sf=','.join(ls)
    le = len(ls)


def ref(res):
    global d1
    d1 = '^', 'lg', 'ln(', 'log_{', '}('
    d2 = '**', 'log10', 'log(', 'flog(', ','
    dic = dict(zip(d1, d2))
    for i in dic:
        res = res.replace(i, dic[i])

    res = replace2mul(res)
    res = replace2abs(res)
    return res


def flog(base, x):
    y = log(x) / log(base)
    return y


def fp(app):
    res1 = ls[0]
    res1 = ref(res1)
    res2 = ls[1]
    res2 = ref(res2)
    ar = ls[2].replace('=','')
    ar=ref(ar)
    lt = ar.split('<')
    if len(lt)==3:
        tn,tm=eval(lt.pop(0)),eval(lt.pop(-1))
    else:
        tn,tm= (-2,2)
    exec(f'{lt[0]} = linspace(tn, tm, n)')
    exec(res1)
    exec(res2)
    # we must use `eval``, as in function local variables are referred by index and here `x`,`y` aren't indexed
    f,=app.au.plot(eval('x'), eval('y'), mode, linewidth=1,picker=1)
    app.df[str(f)]=sf



def fn(app):
    res0 = ls[0]
    res0 = ref(res0)
    rx = ls[1] if le >= 2 else '-2<x<2'
    rx=ref(rx)
    lx = rx.split('<')
    if res0.startswith('y='):
        exp=res0[2:]
        x = linspace(eval(lx[0]), eval(lx[2]), n)
        #except NameError: app.text.insert(0.0,'please check your input')
        y = eval(exp)

        rmtan90(exp,y,x,abs_tol=0.0)
        
        f,=app.au.plot(x, y, mode, linewidth=1,picker=True) 
        app.df[str(f)]=sf
    else:
        x = linspace(eval(lx[0]), eval(lx[-1]), n)
        ry = ls[2] if le >= 3 else '-2<y<2'
        ly = ry.split('<')
        y = linspace(eval(ly[0]), eval(ly[-1]), n)
        x, y = meshgrid(x, y)
        lres = res0.split('=')
        lres[-1] = '({})'.format(lres[-1])
        res0 = '-'.join(lres)
        #except NameError: app.text.insert(0.0,'please check your input')
        z = eval(res0)
        for i in app.au.contour(x, y, z, 0).collections:
            #print(i)
            i.set_picker(2)
            app.df[str(i)]=sf
            
        
    #except RuntimeWarning: app.text.insert(0.0,'please check the domain of definition')

def fshow(app):
    #app.canvas.title('func')
    app.au.axis('equal')
    app.canvas.draw() 

def fmain0(exp,app):
    gets(exp)
    if (le >= 3): 
        if (ls[0].startswith('x=') and ls[1].startswith('y='))or(ls[1].startswith('x=') and ls[0].startswith('y=')):
            fp(app)
    else:
        fn(app)

def fmain(app):
    lf=app.s1.get().split(';')
    if len(lf)!=0 and lf[0]!='':
        for i in lf:
            fmain0(i,app)
        app.s1.set('')
        fshow(app)
