# import json
# from requests.exceptions import HTTPError


def response_hook(response, *args, **kwargs):
    response.raise_for_status()
    return response
    # except HTTPError as exc:
    #     err_msg = str(exc)
    #     try:
    #         error_dict = response.json()
    #     except json.decoder.JSONDecodeError:
    #         pass
    #     else:
    #         if "error" in error_dict:
    #             err_msg += " [Error: {}]".format(error_dict["error"])
    #     raise (err_msg)
    # else:
    #     return response.json()
