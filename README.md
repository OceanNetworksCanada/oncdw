The oncdw Python library provides helper methods for creating data widgets,
which visualize data retrieved from Oceans 3.0 Data Portal.

# Getting started

## Installation

To install the library

```shell
pip install oncdw@git+https://github.com/OceanNetworksCanada/oncdw@main
```

## The ONCDW class

Create an [ONCDW](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/index.html#oncdw.ONCDW)
object to access this library's functionalities.

```python
from oncdw import ONCDW

client = ONCDW()  # Works if the token is set by an env variable ONC_TOKEN
client2 = ONCDW("YOUR_TOKEN")
client3 = ONCDW("YOUR_TOKEN", show_info=True, env="QA")
```

Since the library is based on [streamlit](https://streamlit.io/), to start the server for the app,
run (assume the file name of the script is app.py).

```shell
streamlit run app.py
```
Also, you can add your environment variables (`ONC_TOKEN` in our case) in `.streamlit/secrets.toml` 
by adding a line (double quotes are required).

```
ONC_TOKEN="YOUR_TOKEN"
```

## Widget

Widget class contains the most basic methods to generate plots or tables. They usually get data from Oceans 3.0 Data
Portal
through [OpenAPI](https://data.oceannetworks.ca/OpenAPI) or internal web services, and visualize the data using
plotting libraries ([Vega-Altair](https://altair-viz.github.io/) in our case).

Check [here](https://oncdw-demo.streamlit.app/Demo_Widgets) for the widgets demo.

### [time_series](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.time_series)

The API end point for querying the data is `/ScalarDataAPIService` (Internal).

```python
sensor = {
   "sensor_id": 4182,
}
client.widget.time_series(sensor, "2010-02-18T00:00:00.000Z", "2010-02-21T00:00:00.000Z")
```

### [time_series_two_sensors](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.time_series_two_sensors)

The API end point for querying the data is `/ScalarDataAPIService` (Internal).

```python
sensor1 = {
    "sensor_id": 4182,
}
sensor2 = {
    "sensor_id": 7712,
}
client.widget.time_series_two_sensors(sensor1, sensor2, "-P4D")
client.widget.time_series_two_sensors(4182, 7712, "-P4D")
```

### [table_archive_files](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.table_archive_files)

The API end point for querying the data is `/api/archivefiles` ([OpenAPI](https://data.oceannetworks.ca/OpenAPI#get-/archivefile/location)).

```python
device = {
    "device_code": "CODAR25VATK",
    "file_extensions": ["png", "ruv"],
}
client.widget.table_archive_files(
    device,
    date_from="-P1D",
    date_to="-PT22H",
)
```

### [data_preview](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.data_preview)

The API end point for querying the data is `/DataPreviewService` (Internal).

```python
device = {
    "search_tree_node_id": 450,
    "device_category_id": 72,
}
data_preview_option = {
    "data_product_format_id": 3,
    "plot_number": 1
}
client.widget.data_preview(device, data_preview_option)
```

### [heatmap_archive_files](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.heatmap_archive_files)

The API end point for querying the data is `/api/archivefiles` ([OpenAPI](https://data.oceannetworks.ca/OpenAPI#get-/archivefile/location)).

```python
device = {
    "device_code": "CODAR25VATK",
    "file_extensions": ["tar", "zip"],
}
client.widget.heatmap_archive_files(
    device,
    date_from="-P3D",
)
```

### [scatter_plot_two_sensors](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.scatter_plot_two_sensors)

The API end point for querying the data `/api/scalardata` ([OpenAPI](https://data.oceannetworks.ca/OpenAPI#get-/scalardata/location)).

```python
device = {"location_code": "BACAX", "device_category_code": "CTD"}
sensor_category_codes = "salinity,temperature"
client.widget.scatter_plot_two_sensors(device, sensor_category_codes,date_from="-P1D")
```

### [map](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/widget/index.html#oncdw.widget.Widget.map)

```python
devices = [
    {
        "lat": 48.314627,
        "lon": -126.058106,
        "location_name": "Location X",
        "location_code": "LocationX",
        "device_name": "Device X",
        "device_code": "DeviceX",
    },
    {
        "lat": 50.54427,
        "lon": -126.84264,
        "location_name": "Location Y",
        "location_code": "LocationY",
        "device_name": "Device Y",
        "device_code": "DeviceY",
    },
]

client.widget.map(devices, zoom=6)
```

## UI

UI class provides methods to create labels (based on [shields badges](https://shields.io/)) that have anchor links and
href links.

Check [here](https://oncdw-demo.streamlit.app/Demo_UI) for the UI demo.

### [import_custom_badge_css](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.import_custom_badge_css)

To include a custom css to make labels generated by UI class look bigger.

```python
client.ui.import_custom_badge_css()
```

### [location](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.location)

To display a label for one location.

```python
device = {
    "location_code": "CODE",
    "location_name": "Location Name",
}
client.ui.location(device)
```

### [location_sidebar](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.location_sidebar)

To display a label for one location in the sidebar.

```python
device = {
    "location_code": "CODE",
    "location_name": "Location Name",
}
client.ui.location_sidebar(device)
```

### [device](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.device)

To display a label for one device.

```python
device = {
    "device_id": "12345",
    "device_name": "Device Name",
}
client.ui.device(device)
```

### [device_sidebar](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.device_sidebar)

To display a label for a device in the sidebar.

```python
device = {
    "device_id": "12345",
    "device_code": "CODE"
}
client.ui.device_sidebar(device)
```

### [sensor](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.sensor)

To display a sensor for one sensor.

```python
sensor = {
    "sensor_id": "67900",
    "sensor_name": "Sensor Name"
}
client.ui.sensor_sidebar(sensor)
```

### [sensor_sidebar](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.sensor_sidebar)

To display a label for one sensor in the sidebar.

```python
sensor = {
    "sensor_id": "67900",
    "sensor_name": "Sensor Name"
}
client.ui.sensor_sidebar(sensor)
```

### [sensors_two](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.sensors_two)

To display two labels for two sensors.

```python
sensor1 = {
    "sensor_id": "167900",
    "sensor_name": "Sensor Name 1"
}
sensor2 = {
    "sensor_id": "267900",
    "sensor_name": "Sensor Name 2"
}
client.ui.sensor_sidebar(sensor1, sensor2)
```

### [sensors_two_sidebar](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/ui/index.html#oncdw.ui.UI.sensors_two_sidebar)

To display two labels for two sensors in the sidebar.

```python
sensor1 = {
    "sensor_id": "167900",
    "sensor_name": "Sensor Name 1"
}
sensor2 = {
    "sensor_id": "267900",
    "sensor_name": "Sensor Name 2"
}
client.ui.sensors_two_sidebar(sensor1, sensor2)
```

## Section

Section class provides auxiliary (and opinionated) way to use Widget class and UI class.

Check [here](https://oncdw-demo.streamlit.app/Demo_Sections) for the sections demo.

### [links](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.links)

To display a section with links.

```python
links = {
    "Oceans 3.0": "https://data.oceannetworks.ca",
    "Marine Traffic": "https://www.marinetraffic.com",
}
client.section.links(links, "Useful Links")
```

### [state_of_ocean_images](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.state_of_ocean_images)

To display the State of Ocean images for a given location code.

```python
client.section.state_of_ocean_images("BACAX")
```

### [time_series](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.time_series)

To display time series plots for a given sensor or two sensors, with labels above the plot.

```python
sensor = {
   "sensor_id": 7684,
   "sensor_name": "True Heading",
}
client.section.time_series(sensor)
```

```python
sensor1 = {
    "sensor_id": 4182,
    "sensor_name": "Seafloor Pressure"
}
sensor2 = {
    "sensor_id": 7712,
    "sensor_name": "Uncompensated Seafloor Pressure"
}
sensor = [sensor1, sensor2]
client.section.time_series(sensor)
```

### [data_preview](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.data_preview)

To display data preview plots for multiple data preview options.

```python
device = {
    "search_tree_node_id": 450,
    "device_category_id": 72,
    "data_preview_options": [
        {
            "data_product_format_id": 3,
            "plot_number": 1
        },
        {
            "data_product_format_id": 3,
            "plot_number": 2
        },
    ]
}
client.section.data_preview(device)
```

### [location_expander](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.location_expander)

To display a location label and information retrieved from `/api/location` web service, without duplication.

```python
device = {
    "location_code": "BACAX",
    "location_name": "Barkley Canyon Axis",
}
client.section.location_expander(device)
```

### [location_sidebar](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.location_sidebar)

To display a location badge in the side bar, without duplication.

```python
device = {
    "location_code": "BACAX"
}
client.section.location_sidebar(device)
```

### [sensor_sidebar](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.sensor_sidebar)

Display a sensor or two sensors label in the sidebar, with the correct href link.

```python
sensor = {
   "sensor_id": 7684,
   "sensor_name": "True Heading",
}
client.section.sensor_sidebar(sensor)
```

```python
sensor1 = {
    "sensor_id": 4182,
    "sensor_name": "Seafloor Pressure"
}
sensor2 = {
    "sensor_id": 7712,
    "sensor_name": "Uncompensated Seafloor Pressure"
}
sensor = [sensor1, sensor2]
client.section.sensor_sidebar(sensor)
```

### [map](https://oceannetworkscanada.github.io/oncdw/autoapi/oncdw/section/index.html#oncdw.section.Section.map)

Display a map with a location code.

```python
client.section.map("BACAX")
```
