import autodiff.optimize as opt
import matplotlib.pyplot as plt
import numpy as np

def plot_contour(f, init_val_dict, x,y,plot_range=[-3,3],method = 'gradient_descent'):
    """This function plots a countour map according to the values of 
    expression of interests. It finds the minimum point using either Gradient 
    Descent or Newton's Method and then color it on the contour map.
    
    INPUTS
    =======
    f: expression containing two sub_expressions
    init_val_dict: a dictionary containing variable name and values.
    x: expression 1, represented by x axis
    y: expression 2, represented by y axis
    plot_range: the range of both axes
    method: method with which the function finds the minimum point
    """
    if method == 'gradient_descent':
        a=opt.gradient_descent(f, init_val_dict,return_history=True)
    elif method =='newton':
        a=opt.newton(f, init_val_dict,return_history=True)
    #first plot the contour
    xx=np.linspace(plot_range[0],plot_range[1],100)
    yy=np.linspace(plot_range[0],plot_range[1],100)
    xg,yg = np.meshgrid(xx,yy)
    z=np.zeros(shape=(len(xg.ravel()),))
    for i,val in enumerate(xg.ravel()):
        vals = yg.ravel()
        z[i]=f.evaluation_at({x:val,y:vals[i]})
    z2 = z.reshape(xg.shape)
    plt.contourf(xg, yg, z2, alpha = 0.8, cmap = "BuGn")
    #plot the steps
    f_gd = []
    x_gd = []
    y_gd = []
    for l in a:
        x_gd.append(l[0])
        y_gd.append(l[0])
        #f_gd.append(f.evaluation_at({x:l[0],y:l[1]}))
    plt.plot(x_gd,y_gd,'.',alpha=0.1)
    plt.show()

