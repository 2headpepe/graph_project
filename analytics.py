import pandas as pd
import plotly.graph_objects as go


def read_excel_to_dataframe(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df


file_path = 'graph_algorithms_results_10edges.xlsx'
df = read_excel_to_dataframe(file_path)

# Сравнение времени одного и того же алгоритма при разном Capacity.
capacities = [10, 1000, 10000]
figures = []
for capacity in capacities:
    df_filtered = df[df['Capacity'] == capacity]

    fig = go.Figure()

    # Add Edmonds-Karp data
    fig.add_trace(go.Scatter3d(
        x=df_filtered['Vertices'],
        y=df_filtered['Edges'],
        z=df_filtered['Edmonds-Karp'],
        mode='markers',
        marker=dict(
            size=5,
            color='red',
            opacity=0.8
        ),
        name='Edmonds-Karp'
    ))

    # Add PreFlow data
    fig.add_trace(go.Scatter3d(
        x=df_filtered['Vertices'],
        y=df_filtered['Edges'],
        z=df_filtered['Preflow'],
        mode='markers',
        marker=dict(
            size=5,
            color='blue',
            opacity=0.8
        ),
        name='PreFlow'
    ))

    fig.update_layout(
        title=f'Algorithm Comparison for Capacity {capacity}',
        scene=dict(
            xaxis_title='Vertices',
            yaxis_title='Edges',
            zaxis_title='Time'
        )
    )

    figures.append(fig)

#for fig in figures:
#    fig.show()

# Зависимость времени от количества ребер в графе при константном значении вершин и capacity
df_filtered = df[df['Capacity'] == 1000]
unique_vertices = df_filtered['Vertices'].unique()
figures = []
for vertices in unique_vertices:
    df_vertex = df_filtered[df_filtered['Vertices'] == vertices]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_vertex['Edges'],
        y=df_vertex['Edmonds-Karp'],
        mode='markers+lines',
        marker=dict(
            size=8,
            color='red',
        ),
        name='Edmonds-Karp'
    ))

    fig.add_trace(go.Scatter(
        x=df_vertex['Edges'],
        y=df_vertex['Preflow'],
        mode='markers+lines',
        marker=dict(
            size=8,
            color='blue',
        ),
        name='PreFlow'
    ))

    fig.update_layout(
        title=f'Time Comparison for Vertices: {vertices} and Capacity: 1000',
        xaxis_title='Edges',
        yaxis_title='Time'
    )

    figures.append(fig)
#for fig in figures:
#    fig.show()

unique_vertices = df['Vertices'].unique()
figures = []
for vertices in unique_vertices:
    max_edges = vertices * (vertices - 1) // 2
    df_vertex_edge = df[(df['Vertices'] == vertices) & (df['Edges'] == max_edges)]

    if not df_vertex_edge.empty:
        fig = go.Figure()

        # Edmonds-Karp data
        fig.add_trace(go.Scatter(
            x=df_vertex_edge['Capacity'],
            y=df_vertex_edge['Edmonds-Karp'],
            mode='markers+lines',
            name='Edmonds-Karp',
            marker=dict(
                size=8,
                color='red'
            )
        ))

        # Preflow data
        fig.add_trace(go.Scatter(
            x=df_vertex_edge['Capacity'],
            y=df_vertex_edge['Preflow'],
            mode='markers+lines',
            name='Preflow',
            marker=dict(
                size=8,
                color='blue'
            )
        ))

        fig.update_layout(
            title=f'Time vs Capacity for Vertices: {vertices}, Edges: {max_edges}',
            xaxis_title='Capacity',
            yaxis_title='Time',
            legend_title='Algorithm'
        )
        figures.append(fig)

#for fig in figures:
#    fig.show()

# Зависимость веремени от количества вершин и ребер при разных capacity
fig_ek = go.Figure(data=[go.Scatter3d(
    x=df['Vertices'],
    y=df['Edges'],
    z=df['Edmonds-Karp'],
    mode='markers',
    marker=dict(
        size=5,
        color=df['Edmonds-Karp'],
        colorscale='Viridis',
        colorbar=dict(title='Edmonds-Karp Time'),
        showscale=True
    )
)])

fig_ek.update_layout(
    title='3D Scatter Plot of Edmonds-Karp',
    scene=dict(
        xaxis_title='Vertices',
        yaxis_title='Edges',
        zaxis_title='Time (Edmonds-Karp)'
    )
)

fig_pf = go.Figure(data=[go.Scatter3d(
    x=df['Vertices'],
    y=df['Edges'],
    z=df['Preflow'],
    mode='markers',
    marker=dict(
        size=5,
        color=df['Preflow'],
        colorscale='Viridis',
        colorbar=dict(title='PreFlow Time'),
        showscale=True
    )
)])

fig_pf.update_layout(
    title='3D Scatter Plot of PreFlow',
    scene=dict(
        xaxis_title='Vertices',
        yaxis_title='Edges',
        zaxis_title='Time (PreFlow)'
    )
)

fig_ek.show()
fig_pf.show()

# Зависимость веремени от количества вершин и capacity
fig_ek = go.Figure(data=[go.Scatter3d(
    x=df['Vertices'],
    y=df['Capacity'],
    z=df['Edmonds-Karp'],
    mode='markers',
    marker=dict(
        size=5,
        color=df['Edmonds-Karp'],
        colorscale='Viridis',
        colorbar=dict(title='Edmonds-Karp Time'),
        showscale=True
    )
)])

fig_ek.update_layout(
    title='3D Scatter Plot of Edmonds-Karp',
    scene=dict(
        xaxis_title='Vertices',
        yaxis_title='Capacity',
        zaxis_title='Time (Edmonds-Karp)'
    )
)

fig_pf = go.Figure(data=[go.Scatter3d(
    x=df['Vertices'],
    y=df['Capacity'],
    z=df['Preflow'],
    mode='markers',
    marker=dict(
        size=5,
        color=df['Preflow'],
        colorscale='Viridis',
        colorbar=dict(title='PreFlow Time'),
        showscale=True
    )
)])

fig_pf.update_layout(
    title='3D Scatter Plot of PreFlow',
    scene=dict(
        xaxis_title='Vertices',
        yaxis_title='Capacity',
        zaxis_title='Time (PreFlow)'
    )
)

fig_ek.show()
fig_pf.show()

# Зависимость веремени от количества ребер и capacity
fig_ek = go.Figure(data=[go.Scatter3d(
    x=df['Edges'],
    y=df['Capacity'],
    z=df['Edmonds-Karp'],
    mode='markers',
    marker=dict(
        size=5,
        color=df['Edmonds-Karp'],
        colorscale='Viridis',
        colorbar=dict(title='Edmonds-Karp Time'),
        showscale=True
    )
)])

fig_ek.update_layout(
    title='3D Scatter Plot of Edmonds-Karp',
    scene=dict(
        xaxis_title='Edges',
        yaxis_title='Capacity',
        zaxis_title='Time (Edmonds-Karp)'
    )
)

fig_pf = go.Figure(data=[go.Scatter3d(
    x=df['Edges'],
    y=df['Capacity'],
    z=df['Preflow'],
    mode='markers',
    marker=dict(
        size=5,
        color=df['Preflow'],
        colorscale='Viridis',
        colorbar=dict(title='PreFlow Time'),
        showscale=True
    )
)])

fig_pf.update_layout(
    title='3D Scatter Plot of PreFlow',
    scene=dict(
        xaxis_title='Edges',
        yaxis_title='Capacity',
        zaxis_title='Time (PreFlow)'
    )
)

fig_ek.show()
fig_pf.show()


# Сравнение работы на датасетах
file_path = "test_results.xlsx"
df = pd.read_excel(file_path, index_col=0)

# Transform the DataFrame to have 'Algorithm' as a column for easier plotting
df_reset = df.reset_index().melt(id_vars=['Algorithm'], var_name='Test', value_name='Time (seconds)')

# Create a histogram to compare the two algorithms
fig = go.Figure()

algorithms = df_reset['Algorithm'].unique()
for algorithm in algorithms:
    df_alg = df_reset[df_reset['Algorithm'] == algorithm]
    fig.add_trace(go.Bar(
        x=df_alg['Test'],
        y=df_alg['Time (seconds)'],
        name=algorithm,
        marker=dict(color='red' if algorithm == 'Edmonds-Karp' else 'blue')
    ))

# Update layout for better readability
fig.update_layout(
    title='Algorithm Performance Comparison Across Tests',
    xaxis_title='Test',
    yaxis_title='Time (seconds)',
    barmode='group',
    legend_title='Algorithm'
)

# Show the plot
#fig.show()


