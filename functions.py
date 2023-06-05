import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot(coordinates, truckVector, droneVector, arrivalArray):
    #Creating truck vectors
    truckVectors = []
    for i in range(0,truckVector[0]):
        truckVectors.append([])
        truckVectors[i].append(0)

    #Seperating truck vector
    count = 1
    for i in range(1, truckVector[0]+1):
        for j in range(truckVector[0]+count, truckVector[0]+count+truckVector[i]):
            truckVectors[i-1].append(truckVector[j])
        truckVectors[i-1].append(0)
        count += truckVector[i]

    #Create figure of truck vectors
    fig = go.Figure()

    for i in range(0, truckVector[0]):
        x = []
        y = []
        for j in range(0, len(truckVectors[i])):
            x.append(coordinates[truckVectors[i][j],0])
            y.append(coordinates[truckVectors[i][j],1])

        fig.add_trace(go.Scatter(x=x, y=y, name=F'Truck {i+1}',
                             line=dict(width=3), marker=dict(size=16)))

    #Create figure of truck vectors
    count = 1
    if len(droneVector) > 0:
        for i in range(1, droneVector[0]+1):
            x = []
            y = []
            for j in range(droneVector[0]+count, droneVector[0]+count+droneVector[i]*3, 3):
                x.append(coordinates[droneVector[j], 0])
                y.append(coordinates[droneVector[j], 1])
                x.append(coordinates[droneVector[j+1], 0])
                y.append(coordinates[droneVector[j+1], 1])
                x.append(coordinates[droneVector[j+2], 0])
                y.append(coordinates[droneVector[j+2], 1])

            fig.add_trace(go.Scatter(x=x, y=y, name=F'Drone {i}',
                             line=dict(width=3, dash='dash'), marker=dict(size=20,symbol=2)))

            count +=droneVector[i]*3
    #Depot Marker
    x = []
    y = []
    x.append(coordinates[0,0])
    y.append(coordinates[0,1])
    fig.add_trace(go.Scatter(x=x, y=y, name='DEPOT',
                        marker=dict(size=32, color='darkslategray', symbol=1), mode='markers+text', text="DEPOT", textposition="bottom center"))

    x = []
    y = []
    names = []
    for i in range(1, len(coordinates)):
        x.append(coordinates[i,0])
        y.append(coordinates[i,1])
        names.append(i)
    fig.add_trace(go.Scatter(x=x,y=y,name="names", marker=dict(size=20, color='rgba(0, 0, 0, 0)'), mode = "text+markers", text=names, textposition="top center"))

    fig.update_layout(
    #autosize=False,
    #width=900,
    height=700,
    title="General VNS Solution Visualisation"
    )
    return fig

def gantt_chart(costs, x_max):
    trucks = []

    for i in range(0, len(costs)):
        trucks.append(F"Truck {i+1}")

    df = pd.DataFrame({"Truck Number": list(range(1, len(costs)+1)),
                       "Truck Arrival Time To Depot": costs})

    df['Truck Number'] = df['Truck Number'].astype("str")
    fig = px.bar(df, x = "Truck Arrival Time To Depot", y="Truck Number", color="Truck Number", orientation="h", height=350, range_x=[0, x_max],text="Truck Arrival Time To Depot")

    return fig
