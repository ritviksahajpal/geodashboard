import pandas as pd
import hvplot.pandas
import panel as pn
import os

# Load the CSV file
file_path = r'regional_cei_slope_v3.csv'
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
    print(f"Selected Country: {country}")
    filtered_data = data[data['Country'] == country]
    print(filtered_data.head())  # Debug print to verify filtered data
    regions = filtered_data['Region'].unique().tolist()
    crops = filtered_data['Crop'].unique().tolist()
    
    region_dropdown.options = regions
    crop_dropdown.options = crops
    
    if regions:
        region_dropdown.value = regions[0]
    if crops:
        crop_dropdown.value = crops[0]

# Initial setup of region and crop dropdowns
update_region_and_crop_options(countries[0])

# Function to filter data based on dropdown selections
def update_plot(country, region, crop, season):
    print(f"Selections - Country: {country}, Region: {region}, Crop: {crop}, Season: {season}")
    filtered_data = data[(data['Country'] == country) &
                         (data['Region'] == region) &
                         (data['Crop'] == crop) &
                         (data['Season'] == season)]
    print(filtered_data.head())  # Debug print to verify filtered data
    
    if not filtered_data.empty:
        plot = filtered_data.hvplot.scatter(x='Slope', y='Intercept', hover_cols=['Growth Stage', 'p-value', 'Index', 'Description'])
        print("Plot created successfully.")  # Debug print to verify plot creation
        return plot
    else:
        print("No data available for the selected combination.")  # Debug print for empty data
        return pn.pane.Markdown("No data available for the selected combination.")

# Create the dashboard layout
layout = pn.Column(
    pn.Row(country_dropdown, region_dropdown, crop_dropdown, season_dropdown),
    pn.bind(update_plot, country=country_dropdown, region=region_dropdown, crop=crop_dropdown, season=season_dropdown)
)

# Get the port number from the environment variable
port = int(os.environ.get('PORT', 5006))

# Display the dashboard
if __name__ == '__main__':
    pn.serve(layout, address="0.0.0.0", port=port, allow_websocket_origin=["geodashboard-cc6e73190aa0.herokuapp.com"])
