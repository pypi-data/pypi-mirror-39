import json
import datetime


def print_pretty(json_in):
    pretty_json = json.dumps(json_in, indent=4, sort_keys=True, ensure_ascii=False)
    print(pretty_json)


def datetime_to_odata(datetime_obj):
    return "datetime'" + datetime_obj.strftime('%Y-%m-%dT%H:%M:%S') + "'"


def odatedatetime_to_datetime(odate_datetime):
    return datetime.datetime.strptime(odate_datetime, '%Y-%m-%dT%H:%M:%S')


def odatedate_to_date(odate_date):
    return datetime.datetime.strptime(odate_date, '%Y-%m-%d')


def odateyear_to_date(odate_date):
    return datetime.datetime.strptime(odate_date, '%Y')


def create_api(verbose=False):
    from tkapi.api import Api
    try:
        from local_settings import API_ROOT_URL
        return Api(api_root=API_ROOT_URL, verbose=verbose)
    except ModuleNotFoundError as error:
        return Api(verbose=verbose)
