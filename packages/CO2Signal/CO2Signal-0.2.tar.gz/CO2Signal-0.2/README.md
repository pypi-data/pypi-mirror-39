# CO2Signal
A package to access the co2signal API.

Using this package, you can query the latest CO2 intensity in all the countries or regions, available in https://www.electricitymap.org. The package uses the API available via https://co2signal.com. The intensity can be queried using the code below.

```python
import CO2signal

token = "get yours from co2signal.com"

# query using the country code
CO2Signal.get_latest_carbon_intensity(token, country_code='BE')

# query using the location
CO2Signal.get_latest_carbon_intensity(token, longitude=50, latitude=5)
```


