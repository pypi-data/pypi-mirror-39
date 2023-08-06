import autodiff.optimize as opt
import matplotlib.pyplot as plt
def plot_contour(f, init_val_dict, plot_range=[-3,3],method = 'gradient_descent'):
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
    plt.contourf(xg,yg,z2,alpha=0.8, cmap="BuGn")
    #plot the steps
    f_gd = []
    x_gd =[]
    y_gd =[]
    for l in a:
        x_gd.append(l[0])
        y_gd.append(l[0])
        #f_gd.append(f.evaluation_at({x:l[0],y:l[1]}))
    plt.plot(x_gd,y_gd,'.',alpha=0.1)
    plt.show()

'''Example
x,y = Variable(),Variable()
f= 100.0*(y - x**2)**2 + (1 - x)**2.0
plot_contour(f, {x:-2,y:-1}, plot_range=[-3,3],method = 'gradient_descent')
'''