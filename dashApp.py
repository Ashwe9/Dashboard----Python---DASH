import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import calendar


#-------------------------------------read data-------------------------------------------

data1=pd.DataFrame(pd.read_excel('db/Tableau de Bord_Projets.xlsx','TPS',skiprows=5))
data2=pd.DataFrame(pd.read_excel('db/Tableau de Bord_Projets.xlsx','IPS',skiprows=5))
frames=[data1,data2]
data=pd.concat(frames, ignore_index=True)

client=data['Client']
projet=data['Projet']
famille_process=data['Famille process\nAUTO/INDUS']
type_transfert=data['Type Transfert\nClient/Groupe']
designation_process=data['Désignation process']
reference=data['Référence']
date_reception=data['Date de réception']
date_prequalification=data['Date pré-qualification']
date_lancement_qualification=data['Date lancement qualification']
date_qualification=data['Date qualification']
date_dms_butee=data['DATE DMS / Butée']
respect_delais=data['Respect délais']
performance=data['Performance']
chef_projet=data['Chef de projet']

#------------------------------------------traitement---------------------------------------

#total des process
total_process=projet.count() 

#total process par chef 
def process_chef(name):
   process=0
   for i in range(len(chef_projet)):
      if (str(chef_projet[i])==name):
         process+=1
   return process

tot_chef=[]
for i  in range(len(chef_projet)):
   tot_chef.append(process_chef(str(chef_projet[i])))
#calcul des process qualifiés
def process_qualification():
   process_qualifie=[]
   date_limite='2021-09-30'
   for i in range(len(date_qualification)):
      date_reelle=str(date_qualification[i])
      if (date_reelle=='nat'and date_reelle=='nan') :
         process_qualifie.append(0)
      else:
         if (date_reelle<date_limite):
            process_qualifie.append(1)
         else: 
            process_qualifie.append(0)
   return (process_qualifie)

process_qualifie=[]
process_qualifie=process_qualification()

def total_qualifie():
   tot=0
   for i in range(len(process_qualifie)):
      if (process_qualifie[i]==1):
         tot+=1;
   return tot

#calcul des process non qualifiés
def total_non_qualifie():
   tot=0
   for i in range(len(process_qualifie)):
      if (process_qualifie[i]==0):
         tot+=1;
   return tot

#calcul des process qualifiés par chef de projet 
def total_process_chef_projet(name):
   tot_chef=[]
   total_qualifie_chef=0
   for i in range(len(chef_projet)):
      if (str(chef_projet[i])==name):
         tot_chef.append(process_qualifie[i])
   for i in range(len(tot_chef)):
      if (tot_chef[i]==1):
         total_qualifie_chef+=1
   return total_qualifie_chef

def total_qualifie_chef_projet():
   for i in range(len(chef_projet)):
      projet_qualifie_chef.append(total_process_chef_projet(str(chef_projet[i])))
   return projet_qualifie_chef

projet_qualifie_chef=[]
projet_qualifie_chef=total_qualifie_chef_projet()

#calcul des process non qualifiés par chef de projet
def total_process_non_qualifie_chef_projet(name):
   tot_chef=[]
   total_non_qualifie_chef=0
   for i in range(len(chef_projet)):
      if (str(chef_projet[i])==name):
         tot_chef.append(process_qualifie[i])
   for i in range(len(tot_chef)):
      if (tot_chef[i]==0):
         total_non_qualifie_chef+=1
   return total_non_qualifie_chef

def total_non_qualifie_chef_projet():
   for i in range(len(chef_projet)):
      projet_non_qualifie_chef.append(total_process_non_qualifie_chef_projet(str(chef_projet[i])))
   return projet_non_qualifie_chef

projet_non_qualifie_chef=[]
projet_non_qualifie_chef=total_non_qualifie_chef_projet()


#mois de qualification
month=['Oct 20','Nov 20','Dec 20','Jan 21','Feb 21','Mar 21','Apr 21','May 21','Jun 21','Jul 21','Aug 21','Sep 21']
month_chiffre=['2020-10','2020-11','2020-12','2021-01','2021-02','2021-03','2021-04','2021-05','2021-06','2021-07','2021-08','2021-09']

def process_monthly(month):
   tot_month=[]
   total_qualifie_month=0
   for i in range(len(date_qualification)):
      if ((str(date_qualification[i])[0:7])==month):
         tot_month.append(process_qualifie[i])
   for i in range(len(tot_month)):
      if (tot_month[i]==1):
         total_qualifie_month+=1
   return total_qualifie_month

def total_process_month():
   for i in range(len(month_chiffre)):
      process_mois.append(process_monthly(str(month_chiffre[i])))
   return process_mois

process_mois=[]
process_mois=total_process_month()

#calcul des process qualifiés par client 
def total_process_client(name):
   tot_client=[]
   total_qualifie_client=0
   for i in range(len(client)):
      if (str(client[i])==name):
         tot_client.append(process_qualifie[i])
   for i in range(len(tot_client)):
      if (tot_client[i]==1):
         total_qualifie_client+=1
   return total_qualifie_client

def total_qualifie_client(name):
   projet_qualifie_client=total_process_client(name)
   return projet_qualifie_client

#calcul des process non qualifiés par client
def total_process_non_qualifie_client(name):
   tot_client=[]
   total_non_qualifie_client=0
   for i in range(len(client)):
      if (str(client[i])==name):
         tot_client.append(process_qualifie[i])
   for i in range(len(tot_client)):
      if (tot_client[i]==0):
         total_non_qualifie_client+=1
   return total_non_qualifie_client

def total_non_qualifie_client(name):
   projet_non_qualifie_client=total_process_non_qualifie_client(name)
   return projet_non_qualifie_client


#calcul des process qualifiés par famille process
def total_process_famille(name):
   tot_famille=[]
   total_qualifie_famille=0
   for i in range(len(famille_process)):
      if (str(famille_process[i])==name):
         tot_famille.append(process_qualifie[i])
   for i in range(len(tot_famille)):
      if (tot_famille[i]==1):
         total_qualifie_famille+=1
   return total_qualifie_famille

def total_qualifie_famille(name):
   projet_qualifie_famille=total_process_famille(name)
   return projet_qualifie_famille

#calcul des process non qualifiés par famille process
def total_process_non_qualifie_famille(name):
   tot_famille=[]
   total_non_qualifie_famille=0
   for i in range(len(famille_process)):
      if (str(famille_process[i])==name):
         tot_famille.append(process_qualifie[i])
   for i in range(len(tot_famille)):
      if (tot_famille[i]==0):
         total_non_qualifie_famille+=1
   return total_non_qualifie_famille

def total_non_qualifie_famille(name):
   projet_non_qualifie_famille=total_process_non_qualifie_famille(name)
   return projet_non_qualifie_famille

#calcul des process qualifiés par type transfert
def total_process_transfert(name):
   tot_transfert=[]
   total_qualifie_transfert=0
   for i in range(len(type_transfert)):
      if (str(type_transfert[i])==name):
         tot_transfert.append(process_qualifie[i])
   for i in range(len(tot_transfert)):
      if (tot_transfert[i]==1):
         total_qualifie_transfert+=1
   return total_qualifie_transfert

def total_qualifie_transfert(name):
   projet_qualifie_transfert=total_process_transfert(name)
   return projet_qualifie_transfert

#calcul des process non qualifiés par type transfert
def total_process_non_qualifie_transfert(name):
   tot_transfert=[]
   total_non_qualifie_transfert=0
   for i in range(len(type_transfert)):
      if (str(type_transfert[i])==name):
         tot_transfert.append(process_qualifie[i])
   for i in range(len(tot_transfert)):
      if (tot_transfert[i]==0):
         total_non_qualifie_transfert+=1
   return total_non_qualifie_transfert

def total_non_qualifie_transfert(name):
   projet_non_qualifie_transfert=total_process_non_qualifie_transfert(name)
   return projet_non_qualifie_transfert

#calcul des process durant chaque jour par mois 

def process_details(day):
   process_day=0
   for i in range(len(date_qualification)):
      if ((str(date_qualification[i]))[0:10]==day) :
         process_day+=1
   return process_day

def process_mois_details(mois):
   day=''
   process_detail_mois=[]
   for i in range(1,32):
      if (i>=10):
         day=mois+'-'+str(i)
      else :
         day=mois+'-0'+str(i)
      process_detail_mois.append(process_details(day))
   return process_detail_mois

#--------------------------------------------------graphs---------------------------------------------------

#graph1: qualification process
fig_process_qualifie = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = total_qualifie(),
    domain = {'x': [0, 1], 'y': [0, 1]},
    delta = {'reference': total_process, 'increasing': {'color': "green"},'font': {'size': 24}},
    gauge = {
        'axis': {'range': [None, total_process], 'tickwidth': 1, 'tickcolor': "grey"},
        'bar': {'color': "forestgreen"},
        'bgcolor': "white",
        'borderwidth': 0,
        'bordercolor': "white",
        'steps': [
            {'range': [0, total_process-20], 'color': 'lightpink'},
            {'range': [total_process-20, total_process], 'color': 'lightgreen'}],
        'threshold': {
            'line': {'color': "orange", 'width': 4},
            'thickness': 0.75,
            'value': total_process}}))

fig_process_qualifie.update_layout(font_color='white',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',margin=dict(t=0,l=30,r=30,b=0),height=210)
#graph2: process par chef de projet
fig_process_chef = go.Figure()
fig_process_chef.add_trace(go.Bar(
    x=chef_projet,
    y=tot_chef,
    name='Total Process',
    marker_color='orange'
))

fig_process_chef.add_trace(go.Bar(
    x=chef_projet,
    y=projet_qualifie_chef,
    name='Process Qualifié',
    marker_color='green'
))

fig_process_chef.add_trace(go.Bar(
    x=chef_projet,
    y=projet_non_qualifie_chef,
    name='Process NON Qualifié',
    marker_color='red'
))
fig_process_chef.update_yaxes(range=[0,50])
fig_process_chef.update_layout(title='Qualification des process par chef de projet',font_color='white',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')



fig_process_chef.update_layout(barmode='group', xaxis_tickangle=-45)

#graph3: process par mois 
fig_process_mois = go.Figure()
fig_process_mois.add_trace(go.Scatter(y=process_mois, x=month,
                    mode='lines',
                    name='lines',
                    marker_color='greenyellow',
                    fill='tozeroy'))
fig_process_mois.update_yaxes(range=[0,50])
fig_process_mois.update_layout(title='Qualification des process durant l\'année Octobre--Septembre',font_color='white',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')


#----------------------------------------------application--------------------------------

app = dash.Dash(__name__)

server = app.server



app.layout = html.Div([
   html.Div([
      html.Div([
         html.Img(src=app.get_asset_url('logo.png'))
      ], className='one-third column' ,id='image'),
      html.Div([
      html.H1('Tableau de Bord'),
      ], className='one-half column', id = 'title'),
      html.Div([
            dcc.Graph(figure=fig_process_qualifie,id='fig_process_qualifie'),
         ]),
   ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),
      html.Div([
         html.Div([
            html.H6(children='Total des process',
                     style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{total_process:,.0f}",
                     style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30})
         ], className='card_container three columns',style={'margin-left': '150px'}),

         html.Div([
            html.H6(children='process qualifiés',
                     style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{total_qualifie():,.0f}",
                     style={'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 30})
         ], className='card_container three columns'),

         html.Div([
            html.H6(children='process non qualifiés',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{total_non_qualifie():,.0f}",
                    style={'textAlign': 'center',
                           'color': 'red',
                           'fontSize': 30})
        ], className='card_container three columns'),
         html.Div([
            dcc.Graph(figure=fig_process_chef,id='fig_process_chef'),
            dcc.Graph(figure=fig_process_mois,id='fig_process_mois')
         ])  
      ], className='row flex display'),
      html.Div([
        html.Div([
            html.P('Select client:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'client',
                         multi = False,
                         searchable= True,
                         value='RSA',
                         placeholder= 'Select ',
                         options= [{'label': c, 'value': c}
                                   for c in (client.unique())], className='dcc_compon'),
               dcc.Graph(id = 'pie_client', config={'displayModeBar': 'hover'})
            ], className='create_container four columns',style={'margin-left':'20px'})

      ]),
      html.Div([
        html.Div([
            html.P('Select famille de process:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'famille',
                         multi = False,
                         searchable= True,
                         value='INDUS',
                         placeholder= 'Select ',
                         options= [{'label': c, 'value': c}
                                   for c in (famille_process.unique())], className='dcc_compon'),
               dcc.Graph(id = 'pie_famille', config={'displayModeBar': 'hover'})
            ], className='create_container three columns',style={'margin-left':'20px', 'margin-right':'20px'})
      ]),
      html.Div([
        html.Div([
            html.P('Select type de transfet:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'transfet',
                         multi = False,
                         searchable= True,
                         value='GROUPE',
                         placeholder= 'Select ',
                         options= [{'label': c, 'value': c}
                                   for c in (type_transfert.unique())], className='dcc_compon'),
               dcc.Graph(id = 'pie_transfert', config={'displayModeBar': 'hover'})
            ], className='create_container four columns')
         ]),
      html.Div([
            html.P('Select Année:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'select_année',
                         multi = False,
                         searchable= True,
                         value='2021',
                         placeholder= 'Select ',
                         options= [{'label': an, 'value': an}
                                   for an in range(2020,2050)], className='dcc_compon'),
            html.P('Mois :', className='fix_label', style= {'color': 'white'}),
            dcc.Slider(id = 'select_mois',
                       included=False,
                       updatemode='drag', 
                       tooltip={'always_visible': True},
                       min = 1,
                       max = 12,
                       step = 1,
                       value=1,
                       marks={str(mois): str(mois) for mois in range(1, 13)},
                       className='dcc_compon'),

        ], className='one-half column', id = 'title2',style={'margin-left': '30%'}),
      html.Div([
         dcc.Graph(id='process_detail_mois', config={'displayModeBar': 'hover'})
            ], className='create_container ten columns',style={'margin-left': '10%'})
   ])



@app.callback(Output('pie_client', 'figure'),
              [Input('client','value')])

def update_graph(client):
   process_qualifie_client=total_qualifie_client(client)
   process_non_qualifie_client=total_non_qualifie_client(client)
   colors = ['orange', '#dd1e35']

   return {
        'data': [go.Pie(
            labels=['process qualifiés', 'process non qualifiés'],
            values=[process_qualifie_client,process_non_qualifie_client ],
            marker=dict(colors=colors),
            hoverinfo='label+value',
            textinfo='label+value',
            hole=.7,
            rotation=45,
            #insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title={'text': 'process par client :\n ' + (client),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
   }

@app.callback(Output('pie_famille', 'figure'),
              [Input('famille','value')])

def update_graph(famille):
   process_qualifie_famille=total_qualifie_famille(famille)
   process_non_qualifie_famille=total_non_qualifie_famille(famille)
   colors = ['orange', '#dd1e35']

   return {
        'data': [go.Pie(
            labels=['process qualifiés', 'process non qualifiés'],
            values=[process_qualifie_famille,process_non_qualifie_famille],
            marker=dict(colors=colors),
            hoverinfo='label+value',
            textinfo='label+value',
            hole=.7,
            rotation=45,
            #insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title={'text': 'famille de process :\n ' + (famille),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
   }

@app.callback(Output('pie_transfert', 'figure'),
              [Input('transfet','value')])

def update_graph(transfert):
   process_qualifie_transfert=total_qualifie_transfert(transfert)
   process_non_qualifie_transfert=total_non_qualifie_transfert(transfert)
   colors = ['orange', '#dd1e35']

   return {
        'data': [go.Pie(
            labels=['process qualifiés', 'process non qualifiés'],
            values=[process_qualifie_transfert,process_non_qualifie_transfert],
            marker=dict(colors=colors),
            hoverinfo='label+value',
            textinfo='label+value',
            hole=.7,
            rotation=45,
            #insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title={'text': 'type de transfert :\n ' + (transfert),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
   }

@app.callback(Output('process_detail_mois', 'figure'),
              [Input ('select_année','value')],
              [Input('select_mois','value')])

def update_graph(select_année,select_mois) :
   if((int(select_mois))>=10):
      mois=str(select_mois)
   else :
      mois='0'+str(select_mois)

   mois=str(select_année)+'-'+mois

   days=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

   return{
      'data':[go.Scatter(y=process_mois_details(mois), x=days,
                    marker_color='greenyellow',
                    fill='tozeroy'
      )],
      'layout': go.Layout(
         title={'text': 'Qualification tout au long du mois',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
         xaxis=dict(
                    title='jours',
                    tickmode='linear',
                    showgrid=False),
         yaxis = dict(
                    title = 'process qualifiés',
                    zeroline=True,
                    tickmode='linear'),
         font_color='white',
         plot_bgcolor='rgba(0,0,0,0)',
         paper_bgcolor='rgba(0,0,0,0)'
      )
   }

if __name__ == '__main__':
    app.run_server(debug=False)