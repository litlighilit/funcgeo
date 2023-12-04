<p align="center" >
  <h1 align="center" style="margin:0 auto;">FuncGeo</h1>
</p>
<h5 align="center">to plot functions by inputing mathematical expressings </h5>
<h3 align="right" style="color:blue"> <!--The style doesn't work?!-->
    
</h3>


<br>

## installation & usage
install via these steps:
```sh
git clone https://github.com/litlighilit/funcgeo.git
cd funcgeo/src
```
then you can run it by either the two ways:
```sh
python -m funcgeo
```
or  
```sh
pip install .
f-g
```

## factor :pushpin:
* site-package-supported by matplotlib  
* act in tkinter  
* enable to [change color,linestyle and marker](#change-colorlinestyle-and-marker)(specifically marker) freely  
* [c.txt](/funcgeo/src/c.txt) in src stores [specal markers](#m) used for marker_cg(change marker function)

## operation :black_nib:
### input
> you can input the followings in mathematical convention(in available table)

available|meaning|python expressing
-|-|-
&nbsp;(blank space)|times|*
^|power|**
log_{a}(x)|the log of x to base a(log<sub>a</sub>x))|

examples: y=x log_{2}(x^2)  :arrow_right:  y=x log<sub>2</sub>x<sup>2</sup><!--$\rightarrow y=x log_2 x^2$-->  
&emsp;What's more,you can input something like`y=x,-10<x<10,r--,n=10`to initialize more accurately
### change color,linestyle and marker
click a object,then press right mouse button  
where there will post a menu for you to change the object's color,linestyle and marker  
*<h4 id="m"> specal markers  </h4>*
in c.txt,there are some Greek alphabets to be used as special markers  
### a Hotkey
`ctrl`+`button-1(left mouse button)` to open a exec-interface  

## something to say :envelope:
f-g was created during my Senior-2's holiday(2021)  

originally inspired by [Geogebra](https://geogebra.org/)  

