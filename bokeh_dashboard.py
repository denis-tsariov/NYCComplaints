import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, Legend
from bokeh.plotting import figure

# Load preprocessed data
# CSV columns: month, zipcode, avg_response_time_hours
df = pd.read_csv('dashboard_data.csv')

# Convert month to datetime
df['month'] = pd.to_datetime(df['month'])

# Prepare list of zipcodes (excluding 'ALL')
zipcodes = sorted(df[df['zipcode'] != 'ALL']['zipcode'].unique().astype(str))

# Default zipcodes for dropdowns
zip1_default = zipcodes[0]
zip2_default = zipcodes[1] if len(zipcodes) > 1 else zipcodes[0]

# Prepare data for ALL 2024
monthly_all = df[df['zipcode'] == 'ALL'][['month', 'avg_response_time_hours']]

# Prepare data for selected zipcodes
def get_zipcode_data(zipcode):
    return df[df['zipcode'].astype(str) == zipcode][['month', 'avg_response_time_hours']]

# Initial data sources
source_all = ColumnDataSource(data={
    'month': monthly_all['month'],
    'avg_response_time_hours': monthly_all['avg_response_time_hours'],
})
source_zip1 = ColumnDataSource(data=get_zipcode_data(zip1_default))
source_zip2 = ColumnDataSource(data=get_zipcode_data(zip2_default))

# Create dropdowns
select_zip1 = Select(title="Select Zipcode 1", value=zip1_default, options=zipcodes)
select_zip2 = Select(title="Select Zipcode 2", value=zip2_default, options=zipcodes)

# Create figure
p = figure(title="NYC 311 Response Time by Zipcode (December 2024)", width=800, height=400, 
           x_axis_label="Zipcode", y_axis_label="Avg Response Time (hours)")

# Since we only have one month of data, create a bar chart instead of line plot
from bokeh.models import FactorRange

# Get data for each source
all_data = df[df['zipcode'] == 'ALL']['avg_response_time_hours'].iloc[0] if len(df[df['zipcode'] == 'ALL']) > 0 else 0
zip1_data = df[df['zipcode'] == zip1_default]['avg_response_time_hours'].iloc[0] if len(df[df['zipcode'] == zip1_default]) > 0 else 0
zip2_data = df[df['zipcode'] == zip2_default]['avg_response_time_hours'].iloc[0] if len(df[df['zipcode'] == zip2_default]) > 0 else 0

# Create bar chart data
categories = ['All NYC', f'Zip {zip1_default}', f'Zip {zip2_default}']
values = [all_data, zip1_data, zip2_data]
colors = ['black', 'blue', 'red']

source = ColumnDataSource(data=dict(categories=categories, values=values, colors=colors))

p = figure(x_range=categories, title="NYC 311 Response Time by Zipcode (December 2024)", 
           width=800, height=400, y_axis_label="Avg Response Time (hours)")

bars = p.vbar(x='categories', top='values', width=0.8, color='colors', source=source)

p.xaxis.axis_label = 'Month'
p.yaxis.axis_label = 'Avg Response Time (hours)'
p.legend.location = 'top_left'

# Update function
def update_plot(attr, old, new):
    zip1 = select_zip1.value
    zip2 = select_zip2.value
    
    # Get new data values
    all_data = df[df['zipcode'] == 'ALL']['avg_response_time_hours'].iloc[0] if len(df[df['zipcode'] == 'ALL']) > 0 else 0
    zip1_data = df[df['zipcode'] == zip1]['avg_response_time_hours'].iloc[0] if len(df[df['zipcode'] == zip1]) > 0 else 0
    zip2_data = df[df['zipcode'] == zip2]['avg_response_time_hours'].iloc[0] if len(df[df['zipcode'] == zip2]) > 0 else 0
    
    # Update categories and values
    new_categories = ['All NYC', f'Zip {zip1}', f'Zip {zip2}']
    new_values = [all_data, zip1_data, zip2_data]
    
    source.data = dict(categories=new_categories, values=new_values, colors=['black', 'blue', 'red'])
    p.x_range.factors = new_categories

select_zip1.on_change('value', update_plot)
select_zip2.on_change('value', update_plot)

layout = column(select_zip1, select_zip2, p)
curdoc().add_root(layout)
curdoc().title = "NYC 311 Response Time Dashboard"
