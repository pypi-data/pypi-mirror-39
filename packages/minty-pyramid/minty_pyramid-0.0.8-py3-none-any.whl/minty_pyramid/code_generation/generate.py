from jinja2 import Environment, PackageLoader


def load_template(template_name: str):
    """Load template from template folder.

    :param template_name: template name
    :type template_name: str
    :return: template
    :rtype: jinja2 template
    """
    pkg_loader = PackageLoader(__name__)
    env = Environment(loader=pkg_loader)
    return env.get_template(template_name)


def routes(routes: list, package_name: str):
    """Create `routes.py` for given routes in package.

    :param routes: routes to create file with
    :type routes: list
    :param package_name: package name
    :type package_name: str
    :return: file created
    :rtype: bool
    """
    template = load_template("routes.j2")
    content = template.render(routes=routes)
    return create_file(
        content=content, filename="routes.py", path=f"{package_name}/routes"
    )


def test_routes(routes: list, package_name):
    """Create 'test_routes_routes.py' for given routes in package.

    :param routes: routes to create file with
    :type routes: list
    :param package_name: package name
    :type package_name: str
    :return: file created
    :rtype: bool
    """
    grouped_routes = group_routes_by(routes=routes, param="handler_file")
    t = load_template("test_routes.j2")
    content = t.render(routes=grouped_routes, package_name=package_name)
    return create_file(
        content=content, filename="test_routes.py", path="tests"
    )


def group_routes_by(routes: list, param: str) -> dict:
    """Group routes by parameter.

    Create different groupings to accomodate different templates

    :param routes: routes
    :type routes: list
    :param param: parameter to group by
    :type param: str
    :return: grouped routes
    :rtype: dict
    """
    grouped_routes = {}
    for route in routes:
        grouped_by_param = grouped_routes.get(route[param], [])
        grouped_by_param.append(route)
        grouped_routes[route[param]] = grouped_by_param
    return grouped_routes


def create_file(content, filename: str, path: str):
    """Create file on given location and write content to it.

    :param content: content to write to file
    :type content: str
    :param filename: filename
    :type filename: str
    :param path: path to file
    :type path: str
    """
    filepath = f"{path}/{filename}"

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
        print(f"Created: '{filepath}'")
