#### Definition of all wrappers for 2D plotting

# Histogram and 2D binned statistics
def hist2D(x,y,bin_num=None,density=True,norm=1,c=None,cstat=None,cmap='viridis',a=1,xlim=None,ylim=None,clim=[None,None],xinvert=False,yinvert=False,
			cinvert=False,crotate=False,xlog=False,ylog=False,clog=True,title=None,xlabel=None,ylabel=None,clabel=None,lab_loc=0,ax=None,multi=False):
	import numpy as np
	import matplotlib.colors as clr
	import matplotlib.pyplot as plt
	from .base_func import axes_handler,base_hist2D,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if bin_num is None:
		bin_num=int((len(x))**0.4)
	else:
		bin_num+=1
	norm=norm*len(x)
	if cinvert:
		cmap+='_r'
	X,Y,Z=base_hist2D(x,y,c,bin_num,norm,density,cstat,xlog,ylog)
	if clog:
		plt.pcolormesh(X,Y,Z.T,norm=clr.LogNorm(vmin=clim[0],vmax=clim[1],clip=True),cmap=cmap,alpha=a,rasterized=True)
	else:
		Z[Z==0]=np.nan
		plt.pcolormesh(X,Y,Z.T,vmin=clim[0],vmax=clim[1],cmap=cmap,alpha=a,rasterized=True)
	if clabel is not None:
		cbar=plt.colorbar()
		cbar.set_label(clabel)
		if crotate:
			cbar.ax.invert_yaxis()
	if not multi:
		plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert)
	if ax is not None:
		old_axes=axes_handler(old_axes)

# Image
def img(im,x=None,y=None,bin_num=None,xlim=None,ylim=None,cmap='viridis',clim=[None,None],xinvert=False,yinvert=False,cinvert=False,crotate=False,
		clog=False,title=None,xlabel=None,ylabel=None,clabel=None,lab_loc=0,ax=None,multi=False):
	import numpy as np
	import matplotlib.colors as clr
	import matplotlib.pyplot as plt
	from .base_func import axes_handler,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if cinvert:
		cmap+='_r'
	if x is None:
		x=np.linspace(np.nanmin(im,axis=0),np.nanmax(im,axis=0),len(im[:,0])+1)
	if y is None:
		y=np.linspace(np.nanmin(im,axis=1),np.nanmax(im,axis=1),len(im[0,:])+1)
	plt.pcolormesh(x,y,im,vmin=clim[0],vmax=clim[1],cmap=cmap,rasterized=True)
	if clabel is not None:
		cbar=plt.colorbar()
		cbar.set_label(clabel)
		if crotate:
			cbar.ax.invert_yaxis()
	if not multi:
		plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert)
	if ax is not None:
		old_axes=axes_handler(old_axes)

# Scatter
def scat(x,y,marker_size=20,marker_type='o',a=1,cmap='viridis',xinvert=False,yinvert=False,cinvert=False,xlog=False,ylog=False,xlim=None,ylim=None,
			xlabel=None,ylabel=None,c='k',clabel=None,plabel=None,title=None,lab_loc=0,ax=None,multi=False):
	import numpy as np
	import matplotlib.pyplot as plt
	from .base_func import axes_handler,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if type(x) is not list:
		x=[x]
		y=[y]
	colour=[]
	if c is None:
		for i in range(len(x)):
			colour.append(np.random.uniform(low=0,high=1,size=len(x[i])))
	else:
		if c is not list:
			c=[c]
		if type(c[0]) is not str:
			for i in c:
				colour.append(i)
		else:
			colour=c
	if type(plabel) is not list:
		plabel=[plabel]*len(x)
	if type(marker_size) is not list:
		marker_size=[marker_size]*len(x)
	if type(marker_type) is not list:
		marker_type=[marker_type]*len(x)
	if cinvert:
		cmap+='_r'
	for i in range(len(x)):
		plt.scatter(x[i],y[i],s=marker_size[i],c=colour[i],label=plabel[i],marker=marker_type[i],edgecolors='none',alpha=a,cmap=cmap,rasterized=True)
	if clabel is not None:
		cbar=plt.colorbar()
		cbar.set_label(clabel)
		if crotate:
			cbar.ax.invert_yaxis()
	if not multi:
		plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert)
	if ax is not None:
		old_axes=axes_handler(old_axes)

# Contours encircling the densest part down to a certain percetange 
def sigma_cont(x,y,percent=[68.27,95.45],bin_num=None,c=None,cmap='viridis',xlim=None,ylim=None,clim=[0.33,0.67],xinvert=False,yinvert=False,
				cinvert=False,crotate=False,s=['solid','dashed','dotted'],xlog=False,ylog=False,title=None,xlabel=None,ylabel=None,clabel=None,
				lab_loc=0,ax=None,multi=False):
	import numpy as np
	import matplotlib.cm as cm
	import matplotlib.pyplot as plt
	from .base_func import axes_handler,base_hist2D,percent_finder,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if type(percent) is not list:
		percent=[percent]
	if bin_num is None:
		bin_num=int((len(x))**0.4)
	else:
		bin_num+=1
	if cinvert:
		cmap+='_r'
	cmap=cm.get_cmap(cmap)
	X,Y,Z=base_hist2D(x,y,c,bin_num,1,None,None,xlog,ylog)
	X=(X[:-1]+X[1:])/2
	Y=(Y[:-1]+Y[1:])/2
	CS=[]
	if c is None:
		if len(percent)<4:
			c=['k']*len(percent)
		else:
			if len(s)<4:
				s=['solid']*len(percent)
			c=cmap(np.linspace(clim[0],clim[1],len(percent)))
	else:
		c=cmap(c)
		s=['solid']*len(p)
	if type(clabel) is not list:
		if clabel is None:
			clabel=[str(np.round(p,1))+'%' for p in percent]
		else:
			clabel=[clabel]*len(x)
	for i in range(len(percent)):
		level=[percent_finder(Z,percent[i]/100)]
		CS.append(plt.contour(X,Y,Z.T,level,colors=[c[i],],linewidths=1.5,linestyles=s[i]))
		if clabel[0] is not None:
			CS[i].collections[0].set_label(clabel[i])
	if clabel[0] is not None:
		if c[0]=='k':
			plt.legend(loc=lab_loc)
		else:
			cbar=plt.colorbar()
			cbar.set_label(clabel)
			if crotate:
				cbar.ax.invert_yaxis()
	if not multi:
		plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert)
	if ax is not None:
		old_axes=axes_handler(old_axes)

