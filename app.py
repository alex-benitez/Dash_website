from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image, ImageFile
import base64



ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

with open("./macs0647_final.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
img  = "data:image/jpg;base64," + encoded_string #Black magic I found on stackoverflow
# img = Image.open('./macs0647_final.jpg')
# high_quality = Image.open('./MACS0647/macs0647_color.png') #This is a test to see if loading the iamge withing the function works better

# imgratio = img.size[1]/img.size[0]
# highratio = high_quality.size[0]/img.size[0]


df = pd.read_csv('./MACS0647/macs0647_phot-eazy.ecsv',sep='\s+',
                 index_col='id',comment='#')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP]) 

fullabel = df.columns[df.columns.str.endswith('flux')]
fullabelerr = df.columns[df.columns.str.endswith('fluxerr')]
flux = df.columns[df.columns.str.endswith('flux')]
fluxerr = df.columns[df.columns.str.endswith('fluxerr')]



for i in fullabel:
    if i not in ['f115w_flux', 'f150w_flux', 'f200w_flux', 'f277w_flux', 'f356w_flux', 'f444w_flux']:
        wavelength = [int(i[1:4])*0.001 for i in flux]
    else:
        wavelength = [int(i[1:4])*0.01 for i in flux]


server = app.server
sizediff = 18254/18640

imfig = px.scatter(df,
                   x='x',y='y',
                   opacity=1.,
                   hover_data=[df.index])
imfig.add_layout_image(dict(source=img,
                            xref="x",
                            yref="y",
                            x=0,
                            y=18254,
                            sizex=18640,
                            sizey=18254,
                            sizing="stretch",
                            layer="below",
                            opacity=1.
                            )
                      )

imfig.update_layout(autosize=False  ,width=1000,height=1000)
imfig.update_layout({'plot_bgcolor':'rgba(0,0,0,0)'})#Notice in this one I set the width to the height of the image because it happens to match
imfig.update_xaxes(autorange=True,showgrid=False,showticklabels=False)
imfig.update_yaxes(autorange=True,showgrid=False,showticklabels=False)
imfig.update_yaxes(scaleanchor = "x",scaleratio = 1) #Makes it so aspect ratio is retained when zooming


##############################################################33
app.layout =  dbc.Container( [   
        dbc.Row(
            dbc.Col(html.H1("IDF",style={'textAlign':'center'}))
               ),
        dbc.Row(
            dbc.Col(html.H3("MACS0647 JWST images and photometry including HST images",style={'textAlign':'center'}))
               ),
        dbc.Row(
            dbc.Col(html.Div("Processed images and catalogs by Vasily Kokorev using the grizli pipeline:https://jwst-grizli.s3.amazonaws.com/macs0647/macs0647_index.html",style={'textAlign':'center'}))
               ),
        dbc.Row(
            dbc.Col(html.H3("Cosmic Spring JWST: https://cosmic-spring.github.io",style={'textAlign':'center'}))
               ),
        dbc.Row(
            dbc.Col(html.Div("Pan and zoom on the image, then hover over each object to show its spectral energy distribution (SED): magnitude or flux vs. wavelength.",style={'textAlign':'left'}))
               ),
        dcc.Input(id='object-nmr', type='number', min=1, max=len(df), step=1),
        
        dcc.RadioItems( id='dots-on', 
                       options=[
                           {'label':'On ','value':'On '},
                           {'label':'Off','value':'Off'}],
                       value= 'On ') ,
        
        dbc.Row(
            [   
                
                dbc.Col(
                    html.Div([
                        dcc.Graph(figure=imfig,
                                  id='crossfilter-indicator-scatter',
                                  responsive=False,
                                  hoverData={'points': df.index}
                                 )
                    ], style={'width': '65em', 
                              'display': 'inline-block', 
                                'padding': '2 2',
                             }),width=8
                    ),
                              
                dbc.Col( [
                            
                      html.Div([
                              dcc.Graph(id='sed-plot'),
                          ], style={'display': 'inline-block', 
                                    'width': '25em'
                                  }),
                                   
                                
                      html.Div([
                            dcc.Graph(id='flux-plot'),
                        ], style={'display': 'inline-block', 
                                  'width': '25em'})
                                  ],align='center',width=2)
                
            ],justify='start'
        ),                 
        dbc.Row(
            dbc.Col(html.H5("EAZY SED modeling and phtometric redshifts coming soon.",style={'textAlign':'left'}))
               ),
],fluid=True)


def sed_plot(idx):
    fluxlabel = df.columns[df.columns.str.endswith('flux')]
    # fluxlabel = fluxlabel[:11]
    fluxerrlabel = df.columns[df.columns.str.endswith('fluxerr')]
    # fluxerrlabel = fluxerrlabel[:11]
    y = df.loc[idx][fluxlabel].values
    y_error = df.loc[idx][fluxerrlabel].values
    y = y.astype(float)
    y_error = y_error.astype(float)
    mag = 23.9 -np.log10(y) # Changed the graph to magnitude against wavelength, there's probably a smarter way to do this
    magerr = 2.5*np.log10(1+y_error/y)

    # minmag = df.loc[idx][mag].min()
    # maxmag = df.loc[idx][mag].max()
    
    # error_yval=df.loc[idx][magerr].values
    # yval=df.loc[idx][mag].values# Here i correct in case the magnitude overflows
    # for i in range( len(yval)):
    #     if yval[i] == 99:
    #         yval[i] = error_yval[i]

    figm = px.scatter(x=wavelength,y=mag, #Removed df.loc[idx] before x=wvl
                      error_y=magerr,
                      labels=dict(x='Wavelength(microns)',y='ABmag')
                    )

    figm.update_layout(autosize=False,width=550,height=400)
    # figm.update_yaxes(range=[maxmag*1.1,minmag-0.5]) # Changed this to 1.1

    return figm

def flux_plot(idx):

    minflux = df.loc[idx][flux].min()
    maxflux = df.loc[idx][flux].max()
    
    minfluxerror = df.loc[idx][fluxerr].min()
    maxfluxerror = df.loc[idx][fluxerr].max()

    figa = px.scatter(df.loc[idx],x=wavelength,y=df.loc[idx][flux].values,
                      error_y=df.loc[idx][fluxerr].values,
                      labels=dict(x=r'Wavelength(microns)',y='Flux ('+u'\u00B5'+'Jy)')
                    )

    figa.update_layout(autosize=False,width=550,height=400)
    # figa.update_yaxes(range=[(minflux-minfluxerror)*1.1,(maxflux+maxfluxerror)*1.1])
    figa.update_yaxes(range=[minflux/1.1,maxflux*1.1])

    return figa

@app.callback(
    Output('sed-plot', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
)

def update_sed_plot(hoverData) :
    idx = hoverData['points'][0]['customdata'][0]
    return sed_plot(idx)

@app.callback(
    Output('flux-plot', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
)

def update_flux_plot(hoverData) :
    idx = hoverData['points'][0]['customdata'][0]
    return flux_plot(idx)

@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('object-nmr', 'value'),
)

def zoom_on_scatter(idx):
        xposition = int(df.loc[idx]['x'])
        yposition = int(df.loc[idx]['y'])
        print('zoomed')
        '''
        Attempt at creating a cropped image in order to have higher resolution when 
        zooming in thus providing actual scientific progress
        
        '''
        

        # bgim = crop_image(idx, 500)
        # bgim.save('./test_images/nomer{}.jpg'.format(idx))
        
        # imfig.update_layout(source=bgim,x = xposition - 300, y = yposition - 300,sizex = bgim.size[0], sizey = bgim.size[1])
        # imfig.add_layout_image(dict(source=bgim,
        #                             xref="x",
        #                             yref="y",                            
        #                             x=left,
        #                             y= lower,
        #                             sizex=bgim.size[0],
        #                             sizey=bgim.size[1],
        #                             sizing="stretch",
        #                             layer="above",
        #                             opacity=1.
        #                             )
        #                            )
        
        imfig.update_xaxes(autorange=False,range = [xposition -150, xposition + 150])
        imfig.update_yaxes(autorange=False,range = [yposition -150, yposition + 150])
        return imfig
    
# @app.callback(
#     Output('crossfilter-indicator-scatter','figure'),
#     Input('dots-on','value')
# )

# def changedots(state):
#     print('working')
#     if state == 'Off':
#         imfig.update_layout(hoverdistance = 0)
#         return imfig
#     elif state == 'On ':
#         imfig.update_layout(hoverdistance = -1)
#         return imfig
    
if __name__ == '__main__':
    app.run_server(debug=True)
