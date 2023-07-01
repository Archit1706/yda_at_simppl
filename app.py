# Import packages
import pandas as pd
import plotly.graph_objects as go
# import dash as Dash
from dash import Dash, dcc, html, Input, Output
import dash_mantine_components as dmc
from datetime import timedelta
import plotly.express as px

# Assuming you have the grouped_df DataFrame
# Assuming you have the grouped_df DataFrame
# grouped_df = pd.read_csv('comments_grouped.csv')
# # print(grouped_df.dtypes)
# grouped_df['comment_published_at'] = pd.to_datetime(grouped_df['comment_published_at'], unit='ns', utc=True)
df = pd.read_csv('translated_comments_deepl.csv')
# df.at[0, 'comment_id'] = 'UgxCxCq15G5iNJEui454AaABAg'
# df.loc[0, 'comment_id'] = 'UgxCxCq15G5iNJEui454AaABAg'
df.dropna(subset=['comment_text_english'], inplace=True)
df["parent_id"] = df["comment_id"].str.split(".", n=1, expand=True)[1]
df['comment_id'] = df["comment_id"].str.split(".", n=1, expand=True)[0]
df['published_at'] = pd.to_datetime(df['published_at'])
df['comment_date'] = df['published_at'].dt.date
df['comment_time'] = df['published_at'].dt.time
videos = pd.read_csv('video_data.csv')
comments_grouped = df.groupby('video_id')

# Create an empty DataFrame for grouped data
grouped_df = pd.DataFrame()

# Iterate over each group
for video_id, group in comments_grouped:
    # Merge comments group with corresponding video information
    merged_group = pd.merge(group, videos, on='video_id', how='left')
    
    # Append merged group to the grouped_df
    grouped_df = grouped_df.append(merged_group, ignore_index=True)

grouped_df = grouped_df.rename(columns={'published_at_x': 'comment_published_at', 'like_count_x': 'comment_like_count', 'published_at_y': 'video_published_at', 'like_count_y': 'video_like_count'})

dataframe = pd.read_csv('author_grouped_data.csv')

# Read the video ID and time range options from a CSV file or any other data source
# video_options = pd.read_csv('video_options.csv')
video_ids = ['otCpCn0l4Wo',
 'Fqym-AW8S5E',
 'l-hifFx71sY',
 'bBYkbmo2pLg',
 'BTRzZ_RD8rQ',
 'AL5Zqt5kdSg',
 'ZZdwDInkSOE',
 'f8qFXx_z8cQ',
 'Z49AnoS7C9Q',
 'I5qamYpmODA',
 'FH_AVmxkAk8',
 'eQ4O9gyEJ98',
 'YqATQ-K1wJs',
 '-yp-dPVFpU4',
 'Jr8li6hpC2s',
 'up54rlmwVBs',
 'pMEkhbshYqY',
 'RzUEf1AKdPk',
 '6bSYJ1dxndo',
 'SA_Nih8ubb8',
 'LrWCff-cj_E',
 'YsSOVDW9TpQ',
 '7Adnms4ok4o',
 'KG9htI6yzSs']
time_range_options = [5, 10, 20, 30, 40, 50, 60, 70, 80, 100, 150]  # Example options
# print('💪')
author_ids = ['UC--0QB8berijsto0vL5z8SQ',
    'UCfzLlzRGxSL487ZsK1Q9M4Q',
 'UCP9-ESl_NU-f9iz9Tl_J3oQ',
 'UClITfPFs-1rlUxox-WFaINg',
 'UCok2mMVMAWz_iyWwmjS6d1g',
 'UCjvmMovYq0kavwPEnjB2Q-w',
 'UC705PydTwbiij9gTl9BHdEg',
 'UCFlTuecoyZ0hcAsynp_73Lw',
 'UC3w193M5tYPJqF0Hi-7U-2g',
 'UC3CKhThVWDaprcb3IcnXDfg',
 'UCy21jkrMOJre_W3fvXc0OQw']

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?family=Roboto&display=swap',
        'rel': 'stylesheet'
    },
    {
        'href': 'custom_styles.css',  # Specify the path to your custom CSS file
        'rel': 'stylesheet'
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# App layout
app.layout = dmc.Container([
    dmc.Header(
        height=70, 
        children=[
            dmc.Center(
                style={"height": 70, "width": "100%", "display": "flex", "align-items": "center"},
                children=[
                    dmc.Anchor("SimPPL - Youtube", href="https://simppl.org/", style={"color": "#130f40", "font-size": "24px", 'font-weight': 'bold'}),
                ],
            )], 
        style={"backgroundColor": "#55efc4", "color": "#130f40", "font-size": "24px", 'font-weight': 'bold', 'margin-bottom': '1rem'}
    ),
    dmc.Stack([
        dmc.Title('Analysis of comments on a particular YouTube Video', style={'color': '#800080', 'font-size': '24px'}),

        dmc.Grid(
            gutter="md",
            children=[
                dmc.Select(
                    id='video-id-select',
                    label='Select Video ID',
                    data=[{'label': video_id, 'value': video_id} for video_id in video_ids],
                    placeholder='Select a Video ID',
                    size="sm",
                    value=video_ids[1],
                    style={'margin-bottom': '1rem', 'width': '100%', 'padding': '0.5rem'},
                ),
                dmc.Select(
                    id='time-range-select',
                    label='Select Time Range',
                    data=[
                        {'label': '5 minutes', 'value': 5},
                        {'label': '10 minutes', 'value': 10},
                        {'label': '20 minutes', 'value': 20},
                        {'label': '30 minutes', 'value': 30},
                        {'label': '40 minutes', 'value': 40},
                        {'label': '50 minutes', 'value': 50},
                        {'label': '60 minutes', 'value': 60},
                        {'label': '80 minutes', 'value': 80},
                        {'label': '100 minutes', 'value': 100},

                    ],
                    placeholder='Select a Time Range',
                    size="sm",
                    style={'margin-bottom': '1rem', 'width': '100%', 'padding': '0.5rem'},
                    value=time_range_options[1],
                )
            ]
        ),

        dmc.Grid([
            dmc.Col([
                dmc.Title('Bubble Plot', style={'color': '#0000FF', 'font-size': '20px'}),
                
                dcc.Graph(id='bubble-plot'),
            ], span=12),

            # dmc.Col([
            #     dmc.Title('Scatter Plot', style={'color': '#008000', 'font-size': '20px'}),
            #     dcc.Graph(id='scatter-plot'),
            # ], span=6),
        ], gutter="lg"  ),
        # html.Hr(),
        dmc.Divider(size="sm"),
        dmc.Title('Comment Count by Date', style={'color': '#0000FF', 'font-size': '20px'}),
        
        dcc.Graph(id='count-plot'),
    ]),
    dmc.Divider(size="sm"),
    
    dmc.Stack([
        dmc.Title('Analysis of comments on different videos by a particular Author', style={'color': '#800080', 'font-size': '24px', 'margin-top': '1rem'}),
        dmc.Grid(
            children=[
                dmc.Select(
                    id='author-id-select',
                    label='Select Author ID',
                    data=[{'label': author_id, 'value': author_id} for author_id in author_ids],
                    placeholder='Select an Author ID',
                    size="sm",
                    style={'margin-bottom': '1rem', 'width': '100%', 'padding': '0.5rem'},
                    value='UC--0QB8berijsto0vL5z8SQ',
                )
            ]
        ),
        dcc.Graph(id='author-comments-plot')
        # dcc.Graph(id='comments-plot')
    ])

], 
fluid=True, 
style={'font-family': 'Roboto', 'font-size': '16px', 'color': '#130f40', 'margin': '0', 'max-width': '1200px', 'width': '100%', 'min-height': '100vh', 'box-shadow': '0 0 10px rgba(0, 0, 0, 0.1)', 'background-color': '#dfe6e9'}
)


# Callback for updating the bubble plot
@app.callback(
    Output('bubble-plot', 'figure'),
    Input('video-id-select', 'value'),
    Input('time-range-select', 'value')
)
def update_bubble_plot(video_id='Fqym-AW8S5E', time_range_minutes=20):
    # Specify the video_id group for which you want to create the graph
    video_id_group = video_id

    # Filter the grouped_df for the specific video_id group
    video_group_df = grouped_df[grouped_df['video_id'] == video_id_group]

    # Get the video's published timestamp
    video_published_at = pd.to_datetime(video_group_df['video_published_at'].iloc[0])

    # Sort the comments based on the published timestamp
    video_comments_df = video_group_df.sort_values('comment_published_at')

    # Calculate the range of time after the video was published
    time_range_end = video_published_at + timedelta(minutes=time_range_minutes)
    time_range = pd.date_range(start=video_published_at, end=time_range_end, freq='1min')

    # Filter the comments within the time range after video was published
    comments_within_range = video_comments_df[
        (video_comments_df['comment_published_at'] >= video_published_at) &
        (video_comments_df['comment_published_at'] <= time_range_end)
    ]

    # Convert comment_published_at to string for plotly compatibility
    comments_within_range['comment_published_at'] = comments_within_range['comment_published_at'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    # Group the comments by author_name and count the number of comments
    author_comment_counts = comments_within_range.groupby('author_name').size().reset_index(name='comment_count')

    # Create the bubble plot
    fig = go.Figure(data=go.Scatter(
        x=comments_within_range['comment_published_at'],
        y=comments_within_range['author_name'],
        mode='markers',
        marker=dict(
            size=author_comment_counts['comment_count'],
            sizemode='diameter',
            sizeref=0.1,
            sizemin=1,
            colorscale='Viridis',
            showscale=True
        ),
        text=comments_within_range['author_name'],
        hovertemplate='<b>%{text}</b><br>Published at: %{x}<br>Comment count: %{marker.size}',
    ))

    # Customize the plot layout
    fig.update_layout(
        title=f"Comments Published within {time_range_minutes} Minutes after Video (Video ID: {video_id_group})",
        xaxis_title='Time',
        yaxis_title='Author Name',
        hovermode='closest',
        xaxis=dict(
            tickmode='array',
            tickvals=comments_within_range['comment_published_at'].tolist(),
            ticktext=time_range.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            tickangle=45
        )
    )

    return fig

# Callback for updating the scatter plot
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('video-id-select', 'value'),
#     Input('time-range-select', 'value')
# )
# def update_scatter_plot(video_id='Fqym-AW8S5E', time_range_minutes=20):
    # Specify the video_id group for which you want to create the plots
    video_id_group = video_id

    # Filter the grouped_df for the specific video_id group
    video_group_df = grouped_df[grouped_df['video_id'] == video_id_group]

    # Sort the comments based on the published timestamp
    video_comments_df = video_group_df.sort_values('comment_published_at')

    # Calculate the range of time after the video was published
    time_range = pd.date_range(
        start=video_comments_df['video_published_at'].iloc[0],
        periods=int(time_range_minutes / 5) + 1,
        freq='5T'
    )

    # Filter the comments within the time range after video was published
    comments_within_range = video_comments_df[
        (video_comments_df['comment_published_at'] >= time_range[0]) &
        (video_comments_df['comment_published_at'] <= time_range[-1])
    ]

    # Group the comments by author_channel_id and comment_published_at
    author_groups = comments_within_range.groupby(['author_channel_id', 'comment_published_at'])

    # Create a DataFrame to store the group information
    group_data = pd.DataFrame(columns=['author_channel_id', 'comment_published_at', 'comment_count', 'author_name', 'comment_text'])

    # Iterate over the author groups and calculate the comment count for each group
    for group_name, group_df in author_groups:
        author_channel_id, comment_published_at = group_name
        comment_count = len(group_df)
        author_name = group_df['author_name'].iloc[0]  # Assuming author_name is the same for all comments by the same author
        comment_text = ', '.join(group_df['comment_text'])  # Concatenate the comment texts with a delimiter
        group_data = group_data.append({
            'author_channel_id': author_channel_id,
            'comment_published_at': comment_published_at,
            'comment_count': comment_count,
            'author_name': author_name,
            'comment_text': comment_text
        }, ignore_index=True)

    # Convert the 'comment_count' column to numeric type
    group_data['comment_count'] = pd.to_numeric(group_data['comment_count'])

    # Create the scatter plot using Plotly
    fig = go.Figure(data=go.Scatter(
        x=group_data['comment_published_at'],
        y=group_data['author_name'],
        mode='markers',
        marker=dict(
            size=group_data['comment_count'],
            color=group_data['comment_count'],
            colorscale='Viridis',
            showscale=True,
            sizeref=0.1,
            sizemin=2,
            sizemode='diameter'
        ),
        text=group_data['comment_text'],
        hovertemplate='<b>%{y}</b><br>Published at: %{x}<br>Comment count: %{marker.size}<br>Comments: %{text}'
    ))

    # Configure the plot layout and labels
    fig.update_layout(
        title=f"Coordinated Behavior Among Users (Video ID: {video_id_group})",
        xaxis_title='Time',
        yaxis_title='Author Name'
    )

    # Add dynamic text below the plot
    if len(group_data) == 0:
        fig.add_annotation(
            text="No coordinated behavior detected.",
            xref='paper', yref='paper',
            x=0.5, y=-0.2, showarrow=False
        )
    else:
        fig.add_annotation(
            text="Potential coordinated behavior detected.",
            xref='paper', yref='paper',
            x=0.5, y=-0.2, showarrow=False
        )

    return fig



# # Callback for updating the scatter plot
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('video-id-select', 'value'),
#     Input('time-range-select', 'value')
# )
# def update_scatter_plot(video_id, time_range_minutes):
#     # Specify the video_id group for which you want to create the plots
#     video_id_group = video_id

#     # Filter the grouped_df for the specific video_id group
#     video_group_df = grouped_df[grouped_df['video_id'] == video_id_group]

#     # Sort the comments based on the published timestamp
#     video_comments_df = video_group_df.sort_values('comment_published_at')

#     # Calculate the range of time after the video was published
#     time_range = pd.date_range(
#         start=video_comments_df['video_published_at'].iloc[0],
#         periods=int(time_range_minutes / 5) + 1,
#         freq='5T'
#     )

#     # Filter the comments within the time range after video was published
#     comments_within_range = video_comments_df[
#         (video_comments_df['comment_published_at'] >= time_range[0]) &
#         (video_comments_df['comment_published_at'] <= time_range[-1])
#     ]

#     # Group the comments by author_channel_id and comment_published_at
#     author_groups = comments_within_range.groupby(['author_channel_id', pd.cut(comments_within_range['comment_published_at'], bins=time_range)])

#     # Create a DataFrame to store the group information
#     group_data = pd.DataFrame(columns=['author_channel_id', 'comment_published_at', 'comment_count', 'author_name', 'comment_text'])

#     # Iterate over the author groups and calculate the comment count for each group
#     for group_name, group_df in author_groups:
#         author_channel_id, comment_published_at = group_name
#         comment_count = len(group_df)
#         author_name = group_df['author_name'].iloc[0]  # Assuming author_name is the same for all comments by the same author
#         comment_text = ', '.join(group_df['comment_text'])  # Concatenate the comment texts with a delimiter
#         group_data = group_data.append({
#             'author_channel_id': author_channel_id,
#             'comment_published_at': comment_published_at.mid,
#             'comment_count': comment_count,
#             'author_name': author_name,
#             'comment_text': comment_text
#         }, ignore_index=True)

#     # Convert the 'comment_count' column to numeric type
#     group_data['comment_count'] = pd.to_numeric(group_data['comment_count'])

#     # Create the scatter plot using Plotly
#     fig = go.Figure(data=go.Scatter(
#         x=group_data['comment_published_at'],
#         y=group_data['author_name'],    
#         mode='markers',
#         marker=dict(
#             size=group_data['comment_count'],
#             color=group_data['comment_count'],
#             colorscale='Viridis',
#             showscale=True
#         ),
#         text=group_data['comment_text'],
#         hovertemplate='<b>%{y}</b><br>Published at: %{x}<br>Comment count: %{marker.size}<br>Comments: %{text}'
#     ))

#     # Configure the plot layout and labels
#     fig.update_layout(
#         title=f"Coordinated Behavior Among Users (Video ID: {video_id_group})",
#         xaxis_title='Time',
#         yaxis_title='Author Name'
#     )

#     # Add dynamic text below the plot
#     if len(group_data) == 0:
#         fig.add_annotation(
#             text="No coordinated behavior detected.",
#             xref='paper', yref='paper',
#             x=0.5, y=-0.2, showarrow=False
#         )
#     else:
#         fig.add_annotation(
#             text="Potential coordinated behavior detected.",
#             xref='paper', yref='paper',
#             x=0.5, y=-0.2, showarrow=False
#         )

#     return fig

# Define the callback function to update the count plot
@app.callback(
    Output('count-plot', 'figure'),
    Input('video-id-select', 'value')
)
def update_count_plot(video_id_input='Fqym-AW8S5E'):
    if video_id_input:
        # Filter the 'grouped_df' DataFrame for the specified video ID
        video_comments = grouped_df[grouped_df['video_id'] == video_id_input]

        # Convert the 'comment_date' column to datetime type
        video_comments['comment_date'] = pd.to_datetime(video_comments['comment_date'])

        # Group the DataFrame by 'comment_date' and count the occurrences
        comment_count = video_comments.groupby('comment_date').size().reset_index(name='count')

        # Create the count plot using Plotly Express
        count_plot = px.bar(comment_count, x='comment_date', y='count')

        # Customize the layout
        count_plot.update_layout(
            title='Comment Count by Date - Video ID: {}'.format(video_id_input),
            xaxis_title='Comment Date',
            yaxis_title='Comment Count',
        )

        return count_plot
    else:
        # Return an empty figure if no video ID is selected
        return {}


# @app.callback(
#     Output('author-comments-plot', 'figure'),
#     Input('author-id-select', 'value')
# )
# def update_author_comments_plot(author_id="UCfzLlzRGxSL487ZsK1Q9M4Q"):
#     # Filter the dataframe based on the selected author_id
#     author_data = dataframe[dataframe['author_channel_id'] == author_id]

#     # Extract 'published_at' and 'comment_text' columns as lists
#     published_at = []
#     comment_texts = []
#     comment_ids = []
#     # video_ids = []
#     for _, row in author_data.iterrows():
#         # for time in row['published_at']:
#         #     published_at.append(time)
#         #     comment_texts.append(row['comment_text'])
#         # for id_ in row['comment_id']:
#         #     comment_ids.append(id_)
#         published_at.extend(row['published_at'])
#         comment_texts.extend(row['comment_text'])
#         comment_ids.extend(row['comment_id'])
    
#     print(len(published_at))
#     print(len(comment_texts))
#     print(len(comment_ids))

#     # Create a pandas DataFrame with the comment information
#     comments_df = pd.DataFrame({'published_at': published_at, 'comment_text': comment_texts, 'comment_ids': comment_ids})

#     # Convert 'published_at' to datetime format
#     comments_df['published_at'] = pd.to_datetime(comments_df['published_at'])

#     # Sort the DataFrame by 'published_at'
#     comments_df = comments_df.sort_values('published_at')

#     # Plot the time series using Plotly
#     fig = px.line(comments_df, x='published_at', y='comment_ids', title='Author Comments Time Series',
#                   hover_data=['comment_text'])

#     return fig

# Callback for updating the author comments plot
@app.callback(
    Output('author-comments-plot', 'figure'),
    Input('author-id-select', 'value')
)
def update_author_comments_plot(author_id):
    # Filter the dataframe based on the selected author_id
    author_data = dataframe[dataframe['author_channel_id'] == author_id]
    
    # Extract 'published_at' and 'comment_text' columns as lists
    published_at = []
    comment_texts = []
    comment_ids = []
    for _, row in author_data.iterrows():
        published_at.extend(row['published_at'])
        comment_texts.extend(row['comment_text'])
        comment_ids.extend(row['comment_id'])
    
    # Create a pandas DataFrame with the comment information
    comments_df = pd.DataFrame({'published_at': published_at, 'comment_text': comment_texts, 'comment_ids': comment_ids})
    
    # Convert 'published_at' to datetime format
    comments_df['published_at'] = pd.to_datetime(comments_df['published_at'])
    
    # Sort the DataFrame by 'published_at'
    comments_df = comments_df.sort_values('published_at')
    
    # Plot the time series using Plotly
    fig = px.line(comments_df, x='published_at', y='comment_ids', title='Author Comments Time Series', hover_data=['comment_text'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
