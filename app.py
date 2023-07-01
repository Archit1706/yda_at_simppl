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
df.at[0, 'comment_id'] = 'UgxCxCq15G5iNJEui454AaABAg'
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
time_range_options = [5, 10, 20, 30]  # Example options

# Initialize the app
# external_stylesheets = [dmc.theme.BLUE, dmc.theme.GREEN, dmc.theme.MAGENTA, dmc.theme.YELLOW]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# # App layout
# app.layout = dmc.Container([
#     dmc.Title('Analysis of comments on a particular YouTube Video', color="blue", size="h3"),
#     dmc.Form([
#         dmc.Select(
#             id='video-id-select',
#             label='Select Video ID',
#             options=[{'label': video_id, 'value': video_id} for video_id in video_ids],
#             value=video_options[0]
#         ),
#         dmc.Select(
#             id='time-range-select',
#             label='Select Time Range (minutes)',
#             options=[{'label': str(minutes), 'value': minutes} for minutes in time_range_options],
#             value=time_range_options[0]
#         ),
#     ]),
#     dmc.Grid([
#         dmc.Col([
#             dcc.Graph(id='bubble-plot')
#         ], span=6),
#         dmc.Col([
#             dcc.Graph(id='scatter-plot')
#         ], span=6),
#     ]),
# ])

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?family=Roboto&display=swap',
        'rel': 'stylesheet'
    },
    {
        'href': 'path/to/custom_styles.css',  # Specify the path to your custom CSS file
        'rel': 'stylesheet'
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# App layout
app.layout = dmc.Container([
    dmc.Title('Analysis of comments on a particular YouTube Video', style={'color': '#800080', 'font-size': '24px'}),

    dmc.Grid([
        dmc.Col([
            dmc.Title('Bubble Plot', style={'color': '#0000FF', 'font-size': '20px'}),
            # html.Div([
                dmc.Select(
                    id='video-id-select',
                    label='Select Video ID',
                    data=[{'label': video_id, 'value': video_id} for video_id in video_ids],
                    placeholder='Select a Video ID',
                    size="sm",
                    value=video_ids[0],
                    style={'margin-bottom': '1rem'}
                ),
                dmc.Select(
                    id='time-range-select',
                    label='Select Time Range',
                    data=[
                        {'label': '5 minutes', 'value': 5},
                        {'label': '10 minutes', 'value': 10},
                        {'label': '20 minutes', 'value': 20}
                    ],
                    placeholder='Select a Time Range',
                    size="sm",
                    style={'margin-bottom': '1rem'},
                    value=time_range_options[1]
                ),
            # ]),
            dcc.Graph(id='bubble-plot'),
        ], span=6),

        dmc.Col([
            dmc.Title('Scatter Plot', style={'color': '#008000', 'font-size': '20px'}),
            dcc.Graph(id='scatter-plot'),
        ], span=6),
    ], gutter="md"),
    html.Hr(),
    html.H1("Comment Count by Date"),
    # html.Div([
    #     html.Label("Select Video ID:"),
    #     dcc.Dropdown(
    #         id='video-id-dropdown',
    #         options=[{'label': vid_id, 'value': vid_id} for vid_id in video_ids],
    #         placeholder="Select a video ID",
    #     ),
    # ]),
    dcc.Graph(id='count-plot'),

], fluid=True)


# Callback for updating the bubble plot
@app.callback(
    Output('bubble-plot', 'figure'),
    Input('video-id-select', 'value'),
    Input('time-range-select', 'value')
)
def update_bubble_plot(video_id, time_range_minutes):
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
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('video-id-select', 'value'),
    Input('time-range-select', 'value')
)
def update_scatter_plot(video_id, time_range_minutes):
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
    author_groups = comments_within_range.groupby(['author_channel_id', pd.cut(comments_within_range['comment_published_at'], bins=time_range)])

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
            'comment_published_at': comment_published_at.mid,
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
            showscale=True
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

# Define the callback function to update the count plot
@app.callback(
    Output('count-plot', 'figure'),
    Input('video-id-select', 'value')
)
def update_count_plot(video_id_input):
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)







# # Import the necessary packages
# import pandas as pd
# import plotly.graph_objects as go
# from dash import Dash, dcc, html, Input, Output
# import dash_mantine_components as dmc
# from datetime import timedelta

# # Assuming you have the grouped_df DataFrame
# # grouped_df = pd.read_csv('comments_grouped.csv')
# # # print(grouped_df.dtypes)
# # grouped_df['comment_published_at'] = pd.to_datetime(grouped_df['comment_published_at'], unit='ns', utc=True)
# df = pd.read_csv('translated_comments_deepl.csv')
# df.at[0, 'comment_id'] = 'UgxCxCq15G5iNJEui454AaABAg'
# df.dropna(subset=['comment_text_english'], inplace=True)
# df["parent_id"] = df["comment_id"].str.split(".", n=1, expand=True)[1]
# df['comment_id'] = df["comment_id"].str.split(".", n=1, expand=True)[0]
# df['published_at'] = pd.to_datetime(df['published_at'])
# df['comment_date'] = df['published_at'].dt.date
# df['comment_time'] = df['published_at'].dt.time
# videos = pd.read_csv('video_data.csv')
# comments_grouped = df.groupby('video_id')

# # Create an empty DataFrame for grouped data
# grouped_df = pd.DataFrame()

# # Iterate over each group
# for video_id, group in comments_grouped:
#     # Merge comments group with corresponding video information
#     merged_group = pd.merge(group, videos, on='video_id', how='left')
    
#     # Append merged group to the grouped_df
#     grouped_df = grouped_df.append(merged_group, ignore_index=True)

# grouped_df = grouped_df.rename(columns={'published_at_x': 'comment_published_at', 'like_count_x': 'comment_like_count', 'published_at_y': 'video_published_at', 'like_count_y': 'video_like_count'})


# # Read the video ID and time range options from a CSV file or any other data source
# video_ids = ['otCpCn0l4Wo',
#  'Fqym-AW8S5E',
#  'l-hifFx71sY',
#  'bBYkbmo2pLg',
#  'BTRzZ_RD8rQ',
#  'AL5Zqt5kdSg',
#  'ZZdwDInkSOE',
#  'f8qFXx_z8cQ',
#  'Z49AnoS7C9Q',
#  'I5qamYpmODA',
#  'FH_AVmxkAk8',
#  'eQ4O9gyEJ98',
#  'YqATQ-K1wJs',
#  '-yp-dPVFpU4',
#  'Jr8li6hpC2s',
#  'up54rlmwVBs',
#  'pMEkhbshYqY',
#  'RzUEf1AKdPk',
#  '6bSYJ1dxndo',
#  'SA_Nih8ubb8',
#  'LrWCff-cj_E',
#  'YsSOVDW9TpQ',
#  '7Adnms4ok4o',
#  'KG9htI6yzSs']
# time_range_options = [5, 10, 20, 30]  # Example options

# # Initialize the app
# app = Dash(__name__)

# # App layout
# app.layout = dmc.Container([
#     dmc.Title('Analysis of comments on a particular YouTube Video', style={'color': '#800080', 'font-size': '24px'}),

#     dmc.Grid([
#         dmc.Col([
#             dmc.Title('Bubble Plot', style={'color': '#0000FF', 'font-size': '20px'}),
#             # dmc.Form([
#                 dmc.Select(
#                     id='video-id-select',
#                     label='Select Video ID',
#                     data=[{'label': video_id, 'value': video_id} for video_id in video_ids],
#                     placeholder='Select a Video ID',
#                     size="sm",
#                     value=video_ids[0],
#                     style={'margin-bottom': '1rem'}
#                 ),
#                 dmc.Select(
#                     id='time-range-select',
#                     label='Select Time Range',
#                     data=[
#                         {'label': '5 minutes', 'value': 5},
#                         {'label': '10 minutes', 'value': 10},
#                         {'label': '20 minutes', 'value': 20}
#                     ],
#                     placeholder='Select a Time Range',
#                     size="sm",
#                     style={'margin-bottom': '1rem'},
#                     value=time_range_options[1]
#                 ),
#             # ]),
#             dcc.Graph(id='bubble-plot'),
#         ], span=6),

#                 dmc.Col([
#             dmc.Title('Scatter Plot', style={'color': '#008000', 'font-size': '20px'}),
#             dcc.Graph(id='scatter-plot'),
#         ], span=6),
#     ]),
# ], fluid=True)

# # Callback for updating the bubble plot
# @app.callback(
#     Output('bubble-plot', 'figure'),
#     Input('video-id-select', 'value'),
#     Input('time-range-select', 'value')
# )
# def update_bubble_plot(video_id, time_range):
#     # Filter the comments based on the selected video ID
#     filtered_df = grouped_df[grouped_df['video_id'] == video_id]
    
#     # Calculate the time threshold
#     time_threshold = pd.Timestamp.now() - timedelta(minutes=time_range)
    
#     # Filter the comments based on the time threshold
#     filtered_df = filtered_df[filtered_df['comment_published_at'] >= time_threshold]
    
#     # Create the bubble plot
#     bubble_plot = go.Figure(data=go.Scatter(
#         x=filtered_df['comment_likes'],
#         y=filtered_df['comment_replies'],
#         mode='markers',
#         marker=dict(
#             color=filtered_df['comment_rating'],
#             colorscale='Viridis',
#             showscale=True
#         ),
#         text=filtered_df['comment_text'],
#         hovertemplate=
#         "<b>Comment:</b> %{text}<br><br>" +
#         "<b>Likes:</b> %{x}<br>" +
#         "<b>Replies:</b> %{y}<br>" +
#         "<b>Rating:</b> %{marker.color}<br>",
#         hoverlabel=dict(bgcolor='white'),
#     ))
    
#     bubble_plot.update_layout(
#         title=f'Bubble Plot of Comments for Video ID: {video_id}',
#         xaxis_title='Likes',
#         yaxis_title='Replies',
#     )
    
#     return bubble_plot

# # Callback for updating the scatter plot
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('video-id-select', 'value'),
#     Input('time-range-select', 'value')
# )
# def update_scatter_plot(video_id, time_range):
#     # Filter the comments based on the selected video ID
#     filtered_df = grouped_df[grouped_df['video_id'] == video_id]
    
#     # Calculate the time threshold
#     time_threshold = pd.Timestamp.now() - timedelta(minutes=time_range)
    
#     # Filter the comments based on the time threshold

#     filtered_df = filtered_df[filtered_df['comment_published_at'] >= time_threshold]
    
#     # Create the scatter plot
#     scatter_plot = go.Figure(data=go.Scatter(
#         x=filtered_df['comment_published_at'],
#         y=filtered_df['comment_likes'],
#         mode='markers',
#         marker=dict(
#             color=filtered_df['comment_replies'],
#             colorscale='Viridis',
#             showscale=True
#         ),
#         text=filtered_df['comment_text'],
#         hovertemplate=
#         "<b>Comment:</b> %{text}<br><br>" +
#         "<b>Likes:</b> %{y}<br>" +
#         "<b>Replies:</b> %{marker.color}<br>" +
#         "<b>Published At:</b> %{x}<br>",
#         hoverlabel=dict(bgcolor='white'),
#     ))
    
#     scatter_plot.update_layout(
#         title=f'Scatter Plot of Comments for Video ID: {video_id}',
#         xaxis_title='Published At',
#         yaxis_title='Likes',
#     )
    
#     return scatter_plot

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)


