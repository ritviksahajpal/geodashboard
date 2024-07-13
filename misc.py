import pandas as pd
import hvplot.pandas
import panel as pn

# Load the CSV file
file_path = r'D:\Users\ritvik\projects\GEOGLAM\Output\fao\regional_cei_slope.csv'
data = pd.read_csv(file_path)

# Extract unique values for dropdowns
countries = data['Country'].unique().tolist()

# Create dropdown widgets
country_dropdown = pn.widgets.Select(name='Country', options=countries)
region_dropdown = pn.widgets.Select(name='Region', options=[])
crop_dropdown = pn.widgets.Select(name='Crop', options=[])
season_dropdown = pn.widgets.Select(name='Season', options=data['Season'].unique().tolist())


# Function to update region and crop options based on selected country
@pn.depends(country_dropdown.param.value, watch=True)
def update_region_and_crop_options(country):
    filtered_data = data[data['Country'] == country]
    regions = filtered_data['Region'].unique().tolist()
    crops = filtered_data['Crop'].unique().tolist()

    region_dropdown.options = regions
    crop_dropdown.options = crops


# Function to filter data based on dropdown selections
@pn.depends(country_dropdown.param.value, region_dropdown.param.value, crop_dropdown.param.value,
            season_dropdown.param.value)
def update_plot(country, region, crop, season):
    filtered_data = data[(data['Country'] == country) &
                         (data['Region'] == region) &
                         (data['Crop'] == crop) &
                         (data['Season'] == season)]

    if not filtered_data.empty:
        plot = filtered_data.hvplot.scatter(x='Slope', y='Intercept',
                                            hover_cols=['Growth Stage', 'p-value', 'Index', 'Description'])
        return plot
    else:
        return pn.pane.Markdown("No data available for the selected combination.")


# Create the dashboard
dashboard = pn.Column(
    pn.Row(country_dropdown, region_dropdown, crop_dropdown, season_dropdown),
    update_plot
)

# Display the dashboard
pn.serve(dashboard)
