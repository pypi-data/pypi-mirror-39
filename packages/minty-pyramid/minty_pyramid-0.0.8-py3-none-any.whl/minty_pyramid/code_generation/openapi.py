import json


def parse_routes(oa_file, package_name: str) -> list:
    """Parse OpenAPI file and return a list of routes.

    this function expects the following directory structure in the application:
    `{package_name}/views/{x-view}`
    where `x-view` is the filename for the handlers specified in the OpenAPI
    file.

    :param oa_file: OpenAPI dict
    :type oa_file: dict
    :param package_name: package name
    :type package_name: str
    :return: list of routes
    :rtype: list
    """
    routes = []
    for route in oa_file["paths"]:
        r = oa_file["paths"][route]
        for method in r:
            h_file = r[method]["x-view"]
            handler = r[method]["operationId"]

            out = {
                "route": route,
                "method": method.upper(),
                "handler": handler,
                "renderer": "json",
                "view": f"{package_name}.views.{h_file}.{handler}",
                "handler_file": h_file,
            }
            routes.append(out)
    return routes


def load_json_file(filename: str) -> dict:
    """Load an OpenAPI JSON file.

    :param filename: filename
    :type filename: str
    :return: OpenAPI file
    :rtype: dict
    """
    with open(filename, "r", encoding="utf-8") as jsonfile:
        return json.load(jsonfile)
