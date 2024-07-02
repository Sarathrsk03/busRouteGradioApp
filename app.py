import pandas as pd
import plotly.graph_objects as go
import gradio as gr
import schedule
import time

# Load the dataset




def fetch_dataset():
    url = "https://docs.google.com/spreadsheets/d/1rSiT1pfqLKk4OT-VE2JQ1RCBZX5-TZEU8Slhr_Eqk5Q/export?format=csv"
    dataset = pd.read_csv(url)
    return dataset

def showRoutes(routes:list):
    if "All Routes" in routes:
        filtered_df = df
    else:
        filtered_df = df[(df['ROUTE_NO'].isin(routes))]
        #print(filtered_df)

    fig = go.Figure(go.Scattermapbox(
    lat=filtered_df['LATITUDE'].tolist(),
    lon=filtered_df['LONGITUDE'].tolist(),
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=6
    ),
    hoverinfo="text",
    hovertemplate='<b>ROUTE_NO</b>: %{text}<br><b>Stop_Name</b>: %{customdata}',
    text=filtered_df['ROUTE_NO'].tolist(), 
    customdata=filtered_df['STOP_NAME'].tolist()
    ))
 
    fig.update_layout(
        mapbox_style="open-street-map",
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=12.99468,
                lon=80.25892
            ),
            pitch=0,
            zoom=9
        ),

        
    )
    filtered_df2 = filtered_df[["ROUTE_NO","STOP_NAME","TIMING"]]
    return fig,filtered_df2

df =fetch_dataset()
# Function to update dataset every 12 hours
def update_dataset():
    global df
    df = fetch_dataset()

# Schedule dataset update every 12 hours
schedule.every(12).hours.do(update_dataset)

# Function to continuously run scheduled tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
    


def startGradio():
    Routes=["All Routes"]
    routes = df["ROUTE_NO"].unique().tolist()
    Routes.extend(routes)
    # Create the Gradio interface
    with gr.Blocks() as demo:
        with gr.Column():
            text1 = gr.Text(value="College Bus Route Tracker",interactive=False,show_label=False)
            routes = gr.CheckboxGroup(choices=Routes,label="Routes",value=["All Routes"])

            map_component = gr.Plot(min_width=600)
            table = gr.DataFrame(min_width=600)
            #btn = gr.Button(value="Update Filter")
            text2 = gr.Textbox(value="A app based on the research done by \n1.Sarath Rajan Senthilkumar \n2.Veer Jabak \n3.Gautham Vidyashankar \n4.Divij D\n5.Dr Srisakthi Saravanan",show_label=False,interactive=False)
            
        #demo.load(fn=showRoutes,inputs=[routes],outputs=[map_component,table])
        demo.load(fn=showRoutes,inputs=[routes],outputs=[map_component,table])
        routes.change(fn=showRoutes,inputs=[routes],outputs=[map_component,table])
        #btn.click(fn=showRoutes,inputs=[routes],outputs=[map_component,table])

    demo.launch()

if __name__ == "__main__":
    startGradio()
    run_scheduler()


