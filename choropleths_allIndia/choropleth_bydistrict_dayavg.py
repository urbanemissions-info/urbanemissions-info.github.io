
import geopandas
import mapclassify

import mapclassify as mc
import geoplot.crs as gcrs
import geoplot as gplt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib.cm as cm
import numpy as np




def organize_data(params):
    """
    Creates a geodataframe with data value and shape
    polygon to be plotted

    Parameters
    ----------
    params : class object
        Input/Output parameter definitions.

    Returns
    -------
    geodf : GeoDataFrame
        geodataframe with data value and shape
    polygon to be plotted.

    """
    dist = geopandas.read_file(f'{params.input_path}{params.input_shapefile}')
    dd=pd.read_csv(f'{params.input_path}{params.input_csvfile}')
    dd.columns=['censuscode','data','name']
    geodf=pd.merge(dist,dd,on='censuscode')
    return geodf



def return_colormap(params):
    """
    Create colormap of matplotlib based on number of class and given colorcode

    Parameters
    ----------
    params : class object
        Input/Output parameter definitions.
        
    Returns
    -------
    c_cmap : Object
        matplotlib colormap.

    """
    c = matplotlib.colors.ColorConverter().to_rgb
    color_code=[c("#006837"), c("#1a9850"), c("#66bd63"), c("#fdff00"), c("#ffe833"), c("#ffc566"), c("#ff9933"), c("#f46d43"), c("#d73027"), c("#a50026"), c("#660000")]
    c_cmap = LinearSegmentedColormap.from_list("my_colormap",color_code, N=len(params.classif), gamma=1.0)
    return c_cmap


def get_axes(params):
    """
    

    Parameters
    ----------
    params : class object
        Input/Output parameter definitions.

    Returns
    -------
    da_plt : Matplotlib plot object
        
    mainmap : Matplotlib plot axes
        The mainmap is to be plotted on this axes.
    legend_pos : Matplotlib plot axes
        The legend bars and data ionterval values to be plotted on this axes.
    text_label_pos : Matplotlib plot axes
        Text lables are plotted on this axes, acts as layer over mainmap.

    """
    da_plt=plt
    da_plt.figure(figsize=(params.plotsize['width'],params.plotsize['height']))
    mainmap=da_plt.axes((params.mainmappost['x'],params.mainmappost['y'],params.mainmappost['width'],params.mainmappost['height']), projection=gcrs.PlateCarree(),zorder=10)
    legend_pos=da_plt.axes([params.legendpost['x'],params.legendpost['y'],params.legendpost['width'],params.legendpost['height']],frame_on=False,zorder=10)
    text_label_pos=da_plt.axes([params.textpost['x'],params.textpost['y'],params.textpost['width'],params.textpost['height']],frame_on=False,zorder=10)
    return da_plt,mainmap,legend_pos,text_label_pos

def colorbar_index(ncolors, cmap, labels=None, **kwargs):
    """
    
    This is a convenience function to stop you making off-by-one errors
    Takes a standard colour ramp, and discretizes it,
    then draws a colour bar with correctly aligned labels
    
    Parameters
    ----------
    ncolors : Integer
        Number of colours in the colorbar.
    cmap : colormap object
        Colormap object output from function return_colormap()
    labels : TYPE, optional
        DESCRIPTION. The default is None, data labels from function get_label().
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    colorbar : Matplotlib object
        The legend plotted object, an important function to make the bar color legends.

    """
    
    #cmap = cmap_discretize(cmap, ncolors)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable,**kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    if labels:
        colorbar.set_ticklabels(labels)
    return colorbar

def get_label(params,geodf):
    """
    Classify the input data and generate data labels to be
    marked for the legend color boxes, 

    Parameters
    ----------
    params : class object
        Input/Output parameter definitions.
        
    geodf : GeoDataFrame
        geodataframe with data value and shape

    Returns
    -------
    plot_labels : Data labels object of mapclassify
        data labels from function get_label().

    """
    scheme = mc.UserDefined(geodf['data'], params.classif)
    E=scheme.bins;n=len(E);ns=n-1;Q=list(E);Q.insert(0,0);S=Q[0:n]
    plot_labels = ["%d-%d" % (b, c) for b, c in zip(S,E)]
    plot_labels[0]='< %s' % params.classif[0]                                                                               
    plot_labels[len(plot_labels)-1]='> %s' % params.classif[len(params.classif)-2]
    return plot_labels



def legend_maker(params,legend_pos,geodf):
    """
    Genearte and position the legend based on 
    legend_pos

    Parameters
    ----------
    params : class object
        Input/Output parameter definitions.
    legend_pos : Matplotlib plot axes
        The legend bars and data ionterval values to be plotted on this axes.
    geodf : GeoDataFrame
        geodataframe with data value and shape

    Returns
    -------
    None.

    """
    plot_labels=get_label(params,geodf)
    cb = colorbar_index(ncolors=len(plot_labels), cmap=c_cmap,labels=plot_labels,cax = legend_pos);
    cb.ax.tick_params(labelsize=14)
    cb.ax.set_title(params.legendtitle,fontsize=12,fontweight='bold') 
    return 






def text_label(text_label_pos,params):
    """
    

    Parameters
    ----------
    text_label_pos : Matplotlib plot axes
        Text lables are plotted on this axes, acts as layer over mainmap.
    params : class object
        Input/Output parameter definitions.

    Returns
    -------
    None.

    """
    text_label_pos.text(0.45,0.88, 'India Air Quality Information: 3-day forecasts', fontsize=12,fontweight='bold',ha='center',va='center',color='k', transform =text_label_pos.transAxes)
    text_label_pos.text(0.45,0.85, 'Particulate Matter (PM2.5)', fontsize=18,fontweight='bold',ha='center',va='center',color='k', transform = text_label_pos.transAxes)
    text_label_pos.text(0.45,0.82, f'24hr Average for {params.data_date} ', fontsize=20,fontweight='bold',ha='center',va='center',color='k', transform = text_label_pos.transAxes)
    text_label_pos.text(0.5, 0.6, 'Himalayas', fontsize=12,fontweight='bold',ha='left',va='center',color='k', transform =text_label_pos.transAxes)
    text_label_pos.text(0.08, 0.3, 'Arabian Sea', fontsize=12,fontweight='bold',ha='left',va='center',color='k', transform = text_label_pos.transAxes)
    text_label_pos.text(0.55, 0.3, 'Bay of Bengal', fontsize=12,fontweight='bold',ha='left',va='center',color='k', transform = text_label_pos.transAxes)
    text_label_pos.text(0.45, 0.1, 'India 24hr Standard = 80', fontsize=10,fontweight='bold',ha='left',va='center',color='k', transform = text_label_pos.transAxes)
    text_label_pos.text(0.45, 0.08, 'WHO 24hr Guideline = 40', fontsize=10,fontweight='bold',ha='left',va='center',color='k', transform = text_label_pos.transAxes)
    text_label_pos.text(0.45, 0.06, '(c) UrbanEmissions.Info', fontsize=10,fontweight='bold',ha='left',va='center',color='k', transform = text_label_pos.transAxes)


def plot_map(geodf,da_plt,mainmap,c_cmap,params):
    """
    Major function which does the mainmap plotting of
    chloropleth using geodf dataframe. This also saves
    the final output into png file.

    Parameters
    ----------
    geodf : GeoDataFrame
        geodataframe with data value and shape
    polygon to be plotted.
    da_plt : Matplotlib plot object
    
    mainmap : Matplotlib plot axes
        The mainmap is to be plotted on this axes.
    cmap : colormap object
        Colormap object output from function return_colormap()
    params : class object
        Input/Output parameter definitions.

    Returns
    -------
    None.

    """
    scheme = mc.UserDefined(geodf['data'], params.classif)
    gplt.choropleth(
    geodf, hue='data', projection=gcrs.PlateCarree(),
    edgecolor='#000000', linewidth=.2,
    cmap=c_cmap,
    legend=False, scheme=scheme,ax=mainmap)    
    output_png_file=f'{params.output_path}{params.output_filename_with_format}'
    da_plt.savefig(output_png_file, transparent=False)
    da_plt.close()
    


class bin_create_params:
    plotsize={'width':8.0,'height':9.5}
    mainmappost={'x':0.01,'y':-0.05,'width':1.05,'height':1.03}
    legendpost={'x':0.1,'y':0.02,'width':0.03,'height':0.25}
    textpost={'x':0.01,'y':0.01,'width':1.1,'height':1.1}
    classif=[ 20, 40, 60, 90, 120, 150, 200, 250, 300, 400, 10000]
    input_path='./'
    input_shapefile='district1.shp'
    input_csvfile='data_by_district.csv'
    output_path=input_path
    output_filename_with_format='output_district.png'
    data_date='14Sep2023 Thursday'
    legendtitle="$\mu g/ m^3$"



try:
    params=bin_create_params()
    print('created params')
except Exception as error:
    print(f'error in bin create parameter creation {error}')
        
try:
    geodf=organize_data(params)
    print('completed organize_data')
except Exception as error:
    print(f'error in organize_data {error}')
    
    
try:
    da_plt,mainmap,legend_pos,text_label_pos=get_axes(params)
    print('completed get_axes')
except Exception as error:
    print(f'error in get_axes {error}')
    
try:
    c_cmap=return_colormap(params)
    print('completed return_colormap')
except Exception as error:
    print(f'error in return_colormap {error}')
    
try:
    legend_maker(params,legend_pos,geodf)
    print('completed legend_maker')
except Exception as error:
    print(f'error in legend_maker {error}')
    
try:
    text_label(text_label_pos,params)
    print('completed text_label')
except Exception as error:
    print(f'error in text_label {error}')



try:
    plot_map(geodf,da_plt,mainmap,c_cmap,params)
    print('completed plot_map')
except Exception as error:
    print(f'error in plot_map {error}')





