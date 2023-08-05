from minty import Base
from minty.cqrs import CQRS
from minty.infrastructure import InfrastructureFactory
from pyramid.config import Configurator


def _build_cqrs_setup(cqrs):
    """Create a callable for setting up the "CQRS" methods request objects.

    :param cqrs: A configured CQRS object
    :type cqrs: CQRS
    :return: A function, callable by Pyramid, to register the CQRS
        method(s)
    :rtype: callable
    """

    def setup_cqrs_request(config):
        """Add the CQRS accessors to the Pyramid request objects.

        :param config: Pyramid configurator instance
        :type config: Configurator
        :return: Nothing
        :rtype: None
        """

        def get_query_instance(request, domain: str):
            return cqrs.get_query_instance(domain, context=request.host)

        config.add_request_method(get_query_instance, "get_query_instance")

        def get_command_instance(request, domain: str):
            return cqrs.get_command_instance(domain, context=request.host)

        config.add_request_method(get_command_instance, "get_command_instance")

    return setup_cqrs_request


class Engine(Base):
    """Pyramid configurator."""

    __slots__ = ["config", "domains"]

    def __init__(self, domains: list):
        self.domains = domains
        self.config = None

    def setup(self, global_config: dict, **settings) -> object:
        """Set up the application by loading the injecting the CQRS layer.

        :param global_config: Global configuration
        :type global_config: dict
        :return: Returns the Configurator from Pyramid
        :rtype: object
        """
        infra_factory = InfrastructureFactory(
            settings["minty_service.infrastructure.config_file"]
        )

        cqrs = CQRS(self.domains, infra_factory)

        config = Configurator(settings=settings)
        config.include(_build_cqrs_setup(cqrs))

        # TODO 400/404/500 handlers (JSON Output)
        config.add_tween("minty_pyramid.loader.RequestTimer")

        config.scan()
        self.config = config
        return config

    def main(self) -> object:
        """Run the application by calling the wsgi_app function of Pyramid.

        :raises ValueError: When setup is forgotten
        :return: wsgi app
        :rtype: object
        """
        if self.config is None:
            raise ValueError("Make sure you run setup before 'main'")

        self.logger.info("Creating WSGI application")
        return self.config.make_wsgi_app()


class RequestTimer(Base):
    """Middleware / tween to log request time and count to statsd."""

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        """Log time and count to statsd before and after execution of handler.

        :param request: request
        :type request: class
        :return: response
        :rtype: class
        """
        timer = self.statsd.get_timer()
        timer.start()

        response = self.handler(request)

        try:
            req_name = request.matched_route.name
        except AttributeError:
            req_name = "unknown"

        timer.stop(f"{req_name}.time")

        self.statsd.get_counter().increment(
            f"{req_name}.{response.status_int}.count"
        )

        return response
