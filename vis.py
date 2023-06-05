from functions import *

import os
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

path = 'solutions/'
solutions = os.listdir(path)
solutions.sort()
sol_dict = []
for i in solutions:
	a=i[0:2]
	b=i[3:5]
	c=i[6]
	sol_dict.append({'label': f'{b} Nodes - {a} - {c} Truck', 'value':i})

#Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://www.w3schools.com/w3css/4/w3.css', 'https://www.w3schools.com/lib/w3-colors-2017.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'mTSPD: GVNS'
server = app.server
#App Layout
app.layout = html.Div([
	#Header
	html.Div([
		html.H2('mTSPD: General Variable Neighborhood Search Approach')
	],className='w3-container w3-padding w3-2017-grenadine w3-center'),

	#Body
	#upper
	html.Div([
		html.Div([
			html.Div([
				daq.BooleanSwitch(
					id='switch',
					on=False,
					label='Details',
					labelPosition='top',
					color='#4F84C4'
				),
			], className='w3-container w3-white w3-border w3-margin w3-padding w3-center')
		], className='w3-cell w3-col l1'),

		html.Div([
			html.Div([
				html.Label('Iterations'),
				dcc.Slider(
				id='iter-slider',
				step=None,
				)
			], className='w3-container w3-white w3-border w3-margin w3-padding w3-center')
		], className='w3-cell w3-col l11')

	], className='w3-cell-row w3-col l12'),

	#middle
	html.Div([
		html.Div([
			html.Div([
				dcc.Graph(id = 'vns-visual')
			], className='w3-container w3-white w3-border w3-margin w3-padding')
		], className='w3-cell w3-col l7'),

		html.Div([
			html.Div([
				html.Label(id = 'objective', style={'font-size':30}),
			], className='w3-container w3-white w3-border w3-margin w3-padding'),
			html.Div([
				dcc.Graph(id = 'improvement_chart')
			], className='w3-container w3-white w3-border w3-margin w3-padding'),
			html.Div([
			    dcc.Dropdown(
			        id='excel-list',
			        options=sol_dict,
			        value='T1_25_1.xlsx',
					searchable=True
			    ),
			], className='w3-container w3-white w3-border w3-margin w3-padding')
		], id='genel', className='w3-cell w3-col l5'),

		html.Div([
			html.Div([
				dcc.Graph(id = 'gantt-chart')
			], className='w3-container w3-white w3-border w3-margin w3-padding'),
			html.Div([
				html.Label(id = 'objective2', style={'font-size':30}),
			], className='w3-container w3-white w3-border w3-margin w3-padding'),
			html.Div([
				html.Label(id = 'truck'),
				html.Label(id = 'drone')
			], className='w3-container w3-white w3-border w3-margin w3-padding'),
			html.Div([
				html.Label(id = 'neighbour'),
			], className='w3-container w3-white w3-border w3-margin w3-padding')
		], id='detay', className='w3-cell w3-col l5 w3-hide')
	], className='w3-cell-row w3-col l12'),

])

#Callbacks
@app.callback(
	[Output('vns-visual','figure'),
	 Output('gantt-chart', 'figure'),
	 Output('improvement_chart','figure'),
	 Output('objective', 'children'),
	 Output('objective2', 'children'),
	 Output('truck', 'children'),
	 Output('drone', 'children'),
	 Output('neighbour', 'children')],
	[Input('iter-slider', 'value'),
	 Input('excel-list', 'value')])

#Update Figure
def update_figure(selected_iter, instance):

	df = pd.read_excel(F'solutions/{instance}')
	df.columns = ["iteration","neighbour","truck_vector","drone_vector","objective","objective_list","arrival_array"]
	coordinates = pd.read_excel(f'data/{instance[3:5]}_nodes/{instance[0:5]}.xlsx').to_numpy()
	selected_i = df[df['iteration'] == selected_iter]
	import ast
	truck = selected_i['truck_vector'].values[-1]
	truck = ast.literal_eval(truck)
	drone = selected_i['drone_vector'].values[-1]
	drone = ast.literal_eval(drone)
	neighbour = selected_i['neighbour'].values[-1]
	objective = selected_i['objective'].values[-1]
	objective_list = selected_i['objective_list'].values[-1]
	objective_list = ast.literal_eval(objective_list)
	arrival_array = selected_i['arrival_array'].values[-1]
	best = min(df['objective'])
	fig = plot(coordinates, truck, drone, arrival_array)
	fig.update_layout(transition_duration=500,margin = dict(l = 0, r = 0, t = 80, b = 50))

	fig2 = gantt_chart(objective_list, df.loc[0, 'objective'])
	fig2.update_layout(transition_duration=500,margin = dict(l = 0, r = 0, t = 50, b = 20))

	fig3 = px.line(df, x="iteration", y="objective", height=300)
	fig3.update_traces(mode="markers+lines")
	fig3.update_layout(hovermode="x unified",margin = dict(l = 0, r = 0, t = 60, b = 20))

	return fig,  fig2, fig3, F'Best Found: {best}', F'Objective: {objective}', F'Truck Vector: {truck}',F'Drone Vector: {drone}', F'Iteration: {selected_iter} | Shake Neighborhood: {neighbour}'

@app.callback(
	[Output('iter-slider', 'min'),
	 Output('iter-slider', 'max'),
	 Output('iter-slider', 'value'),
	 Output('iter-slider', 'marks')],
	[Input('excel-list', 'value')]
)
def update_slider(instance):
	df = pd.read_excel(F'solutions/{instance}')
	df.columns = ["iteration","neighbour","truck_vector","drone_vector","objective","objective_list","arrival_array"]
	return df['iteration'].min(),df['iteration'].max(),df['iteration'].max(), {str(it): str(it) for it in df['iteration']}
@app.callback(
	[Output('genel', 'className'),
	 Output('detay', 'className')],
	[Input('switch', 'on')])
def update_output(on):
	if on == True:
		return 'w3-cell w3-col l5 w3-hide', 'w3-cell w3-col l5'
	else:
		return 'w3-cell w3-col l5', 'w3-cell w3-col l5 w3-hide'
#Run Server
if __name__ == '__main__':
	app.run_server(debug=False, dev_tools_props_check=False )
