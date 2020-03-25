SEARCH_QUERY_URL = (
    "https://finder.creodias.eu/resto/api/collections/{collection}/search.json?"
)

ACCESS_TOKEN_URL = "https://auth.creodias.eu/auth/realms/DIAS/protocol/openid-connect/token"

DEFAULT_COLLECTION = "Sentinel5P"

SEARCH_QUERY_DEFAULT_PARAMS = {
    'maxRecords': '10',
    'instrument': 'TROPOMI',
    'productType': 'L2__SO2___',
    'timeliness': 'Near+real+time',
    'sortParam': 'startDate',
    'sortOrder': 'descending',
    'status': 'all',
    'dataset': 'ESA-DATASET'
}

SEARCH_QUERY_VARIABLE_PARAMS_EXAMPLE = {
    'startDate': '2019-08-28T00:00:00',
    'completionDate': '2019-08-29T23:59:59',
    'lat': '38.789',
    'lon': '15.213'
}

ACCESS_TOKEN_REQUEST_DEFAULT_PARAMS = {
    'client_id': 'CLOUDFERRO_PUBLIC',
    'username': 'pbpdcpgthvbnkxzzte@awdrt.net',
    'password': 'siema1XD',
    'grant_type': 'password'
}

TSV_FILE_NAME = "volcano-events-2020-03-24_15-08-21_+0100.tsv"

FINDER_QUERY_EXAMPLE = "https://finder.creodias.eu/resto/api/collections/Sentinel5P/search.json?maxRecords=10&startDate=2019-08-28T00:00:00Z&completionDate=2019-08-29T23:59:59Z&lat=38.789&lon=15.213&instrument=TROPOMI&productType=L2__SO2___&timeliness=Near+real+time&sortParam=startDate&sortOrder=descending&status=all&dataset=ESA-DATASET"

