from sgmarkets_api_analytics_rates._obj_from_dict import ObjFromDict
from sgmarkets_api_analytics_rates.request_curves_price import RequestCurvesPrices
from sgmarkets_api_analytics_rates.response_curves_price import ResponseCurvesPrice
from sgmarkets_api_analytics_rates.slice_curves_price import SliceCurvesPrice
from sgmarkets_api_analytics_rates.request_curves_custom import RequestCurvesCustom

dic_endpoint = {
    'v1_curves_price': {
        'request': RequestCurvesPrices,
        'response': ResponseCurvesPrice,
        'slice': SliceCurvesPrice
    },
    'v1_custom_prices': {
        'request': RequestCurvesCustom,
        'response': ResponseCurvesPrice,
        'slice': SliceCurvesPrice
    },
}

endpoint = ObjFromDict(dic_endpoint)

if __name__ == '__main__':
    ep = endpoint
    ep.v1_custom_prices.request()
