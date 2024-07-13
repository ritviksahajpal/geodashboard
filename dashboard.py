import pandas as pd
import hvplot.pandas
import panel as pn

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
    print(filtered_data)
    regions = filtered_data['Region'].unique().tolist()
    crops = filtered_data['Crop'].unique().tolist()
    
    region_dropdown.options = regions
    crop_dropdown.options = crops
    
    if regions:
        region_dropdown.value = regions[0]
    if crops:
        crop_dropdown.value = crops[0]

# Function to filter data based on dropdown selections
@pn.depends(country_dropdown.param.value, region_dropdown.param.value, crop_dropdown.param.value, season_dropdown.param.value)
def update_plot(country, region, crop, season):
    print(f"Selections - Country: {country}, Region: {region}, Crop: {crop}, Season: {season}")
    filtered_data = data[(data['Country'] == country) &
                         (data['Region'] == region) &
                         (data['Crop'] == crop) &
                         (data['Season'] == season)]
    print(filtered_data)
    
    if not filtered_data.empty:
        plot = filtered_data.hvplot.scatter(x='Slope', y='Intercept', hover_cols=['Growth Stage', 'p-value', 'Index', 'Description'])
        return plot
    else:
        return pn.pane.Markdown("No data available for the selected combination.")

# Initial setup of region and crop dropdowns
update_region_and_crop_options(countries[0])

# Create the dashboard
dashboard = pn.Column(
    pn.Row(country_dropdown, region_dropdown, crop_dropdown, season_dropdown),
    update_plot
)

# Display the dashboard
pn.serve(dashboard)
