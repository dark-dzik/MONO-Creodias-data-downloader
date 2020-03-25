# MONO-Creodias-data-downloader

Utility loading list of volcanic eruptions from attached *.tsv file and downloading available satelite data concerning these eruptions from Creodias API.

## Running the utility

It is recommended to run the utility within Python IDE (like PyCharm).

In order to run the utility properly, following Python libraries are required:
- requests
- json
- datetime
- dateutil
- csv

## Downloaded data

Data downloaded by the utility is stored inside project directory, in folder <i>data</id>.

## Additional info

At this moment there are no web requests handling or storage space check precautions implemented.
