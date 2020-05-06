import datetime
from src.queries_handler import build_get_request, build_post_request, get_json_string
from src.storage_handler import create_data_directory, store_json, download, load_tsv
from src.utils import add_seven_days, parse_date
from src.hardcoded_resources import SEARCH_QUERY_URL, SEARCH_QUERY_DEFAULT_PARAMS, DEFAULT_COLLECTION, ACCESS_TOKEN_URL, ACCESS_TOKEN_REQUEST_DEFAULT_PARAMS
from src.extract_geojson import iterate_over_dirs
from src.chrs_handler import download_chrs

##
# Constructs dictionary containing variable params required by creodias finder search query
#
# @params: eruption_tuple - tuple containing eruption data, generated by *.tsv loader function
# @returns: dictionary containing search request params
def prepare_eruption_params(eruption_tuple):
    eruption_params = {
        'startDate': parse_date(datetime.datetime(int(eruption_tuple[1]), int(eruption_tuple[2]), int(eruption_tuple[3]))).isoformat(),
        'completionDate': add_seven_days(parse_date(datetime.datetime(int(eruption_tuple[1]), int(eruption_tuple[2]), int(eruption_tuple[3])))).isoformat(),
        'lat': eruption_tuple[4],
        'lon': eruption_tuple[5]
    }
    return eruption_params


##
# Constructs eruption name string out of eruption tuple.
#
# @param: eruption_tuple - tuple containing eruption data, generated by *.tsv loader function
# @returns: string containing eruption name in following form:
#   <volcano_name>_<year_of_eruption>-<month>-<day>
def prepare_eruption_name(eruption_tuple):
    return eruption_tuple[0] + '_' + eruption_tuple[1] + '-' + eruption_tuple[2] + '-' + eruption_tuple[3]


##
# Checks how many results creodias finder returned and returns its number.
#
# @param: search_query_results - json string containing results of creodias finder search query
# @returns: string stating how many results found
def how_many_search_results(search_query_result_json):
    total_results = search_query_result_json["properties"]["totalResults"]
    print("Results found: %s" % total_results)
    return total_results


##
# Picks urls to search results and returns them as tuple.
#
# @param: search_query_results - json string containing results of creodias finder search query
# @returns: 3-elem tuple with following structure:
#   (<id_of_data_package_from_search_results>, <url_to_package>, <json_describing_data>)
def select_search_results_to_download(search_query_result_json):
    features = list()
    for feature in search_query_result_json["features"]:
        features.append((feature["id"], feature["properties"]["services"]["download"]["url"], feature, feature["properties"]["completionDate"]))
    return features


##
# Attaches creodias collection name to search request.
#
# @param: search_request_url
# @param: collection - creodias finder collection name, i.e. 'Sentinel5P'
# @returns: search request url containing proper collection name
def append_collection_to_search_request(search_request_url, collection):
    return search_request_url.format(collection=collection)


##
# Iterates over list of search results and downloads data packages.
#
# @param: results_to_download_tuple_list - list of tuples generated from search results,
#   tuple structure should be following:
#   (<id_of_data_package_from_search_results>, <url_to_package>, <json_describing_data>)
# @param: download_access_token - creoadias access token for downloading data, required for query builder
# @param: eruption_name - name of the eruption servers directory/file name
def manage_results_download(results_to_download_tuple_list, download_access_token, eruption_data):
    for result in results_to_download_tuple_list:
        data_download_request = build_get_request(result[1], {'token': download_access_token}, True)
        store_json(eruption_data, result[3], result[2])
        download(eruption_data, result[3], data_download_request)


##
# What happens here, line by line:
# *.tsv containing eruptions data is loaded and stored in list of 5-elem tuples
# for each eruption
# select tuple elements and construct eruption name
# select tuple elements and costruct search query params
# merge fixed params with variable params
# set collection value in search query -> Sentinel5P
# build and execute search GET request
# parse received response containing search results to json string
# select download links along identifying data from search results
# build and execute POST request for access token (downloading permitted for logged in only)
# select token from response
# store search query response as *.json
# for each search results
# store its describing *.json
# download and store its data package
def main():
    create_data_directory()
    eruptions_list = load_tsv()
    if len(eruptions_list) > 0:
        for eruption in eruptions_list:
            eruption_name = prepare_eruption_name(eruption)
            eruption_params = prepare_eruption_params(eruption)
            print("\nLooking for %s data \n" % eruption_name)
            search_request_params = {**eruption_params, **SEARCH_QUERY_DEFAULT_PARAMS}
            search_query_url = append_collection_to_search_request(SEARCH_QUERY_URL, DEFAULT_COLLECTION)
            search_request = build_get_request(search_query_url, search_request_params)
            search_results_json_string = get_json_string(search_request.text)

            if search_results_json_string is not None and how_many_search_results(search_results_json_string) > 0:
                results_to_download_tuple_list = select_search_results_to_download(search_results_json_string)
                access_token_request = build_post_request(ACCESS_TOKEN_URL, ACCESS_TOKEN_REQUEST_DEFAULT_PARAMS)
                access_token = get_json_string(access_token_request.text)['access_token']

                store_json(eruption_name, '', search_results_json_string)
                manage_results_download(results_to_download_tuple_list, access_token, eruption_name)


# if __name__ == "__main__":
#     # iterate_over_dirs()
#     download_chrs()
#     # main()
