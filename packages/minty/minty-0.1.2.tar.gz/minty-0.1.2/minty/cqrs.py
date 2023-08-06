import uuid
from abc import ABC, abstractmethod
from functools import partial

from . import Base
from .infrastructure import InfrastructureFactory
from .repository import RepositoryFactory


def event(name: str):
    def register_event(f):
        f.minty_event_name = name
        return f

    return register_event


class Event(Base):
    __slots__ = ["domain", "event_name", "parameters", "uuid"]

    def __init__(self, domain, event_name, parameters):
        self.domain = domain
        self.event_name = event_name
        self.parameters = parameters
        self.uuid = uuid.uuid4()
        self.logger.info(
            f"Event created. Domain = '{domain}', "
            + f"event = '{event_name}', "
            + f"uuid = '{self.uuid}', "
            + f"parameters = '{parameters}'"
        )


class MiddlewareBase(Base, ABC):
    __slots__ = ["infrastructure_factory", "context"]

    def __init__(self, infrastructure_factory=None, context=None):
        """Initialize class with infrastructure_factory and context.

        :param infrastructure_factory: infra structure factory, defaults to None
        :param infrastructure_factory: InfrastructureFactory, optional
        :param context: context, defaults to None
        :param context: dict, optional
        """
        self.infrastructure_factory = infrastructure_factory
        self.context = context

    @abstractmethod
    def __call__(self, func, event: Event, domain: str):
        """Call instantiated class.

        Override this method (including the defined params) in your middleware
        class. The logic or functionality you want to implement should go
        before and after your call to `func()`.

        :param func: function to execute
        :type func: partial function
        :param event: event
        :type event: Event
        :param domain: domain
        :type domain: str
        """
        pass


class InfrastructureStateManager(MiddlewareBase):
    """Set current event in infrastructure factory and clear it after the event is finished.

    Set the event in the infrastructure_factory so different layers can
    retrieve the cached infrastructure session(s)

    :param MiddlewareBase: middleware base class
    :type MiddlewareBase: MiddlewareBase
    """

    def __call__(self, func, event: Event, domain: str):
        self.infrastructure_factory.set_current_event(event)
        func()
        self.infrastructure_factory.flush_current_event()


class TimeFunctionCall(MiddlewareBase):
    """Time and log function call to statsd.

    :param MiddlewareBase: middleware base class
    :type MiddlewareBase: MiddlewareBase
    """

    def __call__(self, func, event: Event, domain: str):
        """Execute, time and log function call."""
        timer = self.statsd.get_timer(domain)
        with timer.time(f"{event.event_name}.execute"):
            func()


class CommandWrapper(Base):
    """Wrapper class for command instances. Handles creation of Events."""

    def __init__(self, domain, command_instance):
        self.domain = domain
        self.command_instance = command_instance
        self.middlewares = []

    def register_middleware(self, middleware: MiddlewareBase):
        """Register middleware to be wrapped around command.

        From inner to outer layer, the last middleware class to get registered will be
        the outer shell and will be executed first and last.

        :param middleware: middleware to register
        :type middleware: MiddlewareBase
        """
        self.middlewares.append(middleware)

    def __getattr__(self, attr):
        """Get an attribute on the wrapped class, wrapped by "event" code.

        This event code ensures the command can't return anything, and creates
        an Event instance.

        :param attr: attribute to retrieve
        :type attr: str
        :return: wrapped method
        :rtype: callable
        """
        orig_attr = self.command_instance.__getattribute__(attr)
        if callable(orig_attr):

            def wrapped(*args, **kwargs):
                """Return attribute wrapped in middlewares."""
                event_name = orig_attr.minty_event_name
                event = Event(self.domain, event_name, kwargs)

                wrapped_func = partial(orig_attr, **kwargs)
                for middleware in self.middlewares:
                    wrapped_func = partial(
                        middleware,
                        func=wrapped_func,
                        event=event,
                        domain=self.domain,
                    )

                wrapped_func()

                return

            return wrapped
        else:
            return orig_attr


class CQRS(Base):
    """Keep commands and queries separated.

    CQRS: Command Query Responsibility Separation
    """

    __slots__ = [
        "domains",
        "infrastructure_factory",
        "command_wrapper_middleware",
    ]

    def __init__(
        self,
        domains,
        infrastructure_factory: InfrastructureFactory,
        command_wrapper_middleware=None,
    ):
        """Create a new CQRS instance from a list of domains.

        :param domains: iterable returning domains. Domains are classes or
            packages with at least a "REQUIRED_REPOSITORIES" variable defining
            which repositories are necessary to use the domain.
        :type domains: object
        :param infrastructure_factory: Infrastructure factory, created with
            the required configuration, that the repositories can use to
            create infrastructure instances.
        :type infrastructure_factory: InfrastructureFactory
        :param command_wrapper_middleware: Middlewares to be wrapped around command
        :type command_wrapper_middleware: list of MiddlewareBase
        """
        self.domains = {}

        if command_wrapper_middleware is None:
            command_wrapper_middleware = []
        self.command_wrapper_middleware = command_wrapper_middleware

        self.infrastructure_factory = infrastructure_factory

        for domain in domains:
            repo_factory = RepositoryFactory(infrastructure_factory)

            for repo in domain.REQUIRED_REPOSITORIES:
                repo_factory.register_repository(repo)

                for infra in repo.REQUIRED_INFRASTRUCTURE:
                    infrastructure_factory.register_infrastructure(infra)

            self.domains[domain.__name__] = {
                "module": domain,
                "repository_factory": repo_factory,
            }

    def get_query_instance(self, domain: str, context=None):
        """Instantiate and return the "query" part of the specified domain.

        :param domain: name of the domain to get the query instance for
        :type domain: str
        :param context: context for this domain, defaults to None
        :param context: object, optional
        """
        # This can probably be cached (per context = host)

        self.logger.debug(
            f"Creating query instance for domain '{domain}' with context "
            + f"'{context}'"
        )

        with self.statsd.get_timer(domain).time("get_query_instance"):
            query_instance = self.domains[domain]["module"].get_query_instance(
                self.domains[domain]["repository_factory"], context=context
            )

        return query_instance

    def get_command_instance(self, domain: str, context=None):
        """Instantiate and return the "command" instance of the specified domain.

        Command instance is instantiated with optional layers of middleware to handle
        various functions when executing a command. `InfrastructureStateManager` is
        always registerd as the outermost layer & `TimeFunctionCall` is always
        registered as the innermost layer.

        :param domain: name of the domain to get the query instance for
        :type domain: str
        :param context: context for this domain, defaults to None
        :param context: object, optional
        """
        self.logger.debug(
            f"Creating command instance for domain '{domain}' with context "
            + f"'{context}'"
        )
        with self.statsd.get_timer(domain).time("get_command_instance"):
            cmd_instance = self.domains[domain]["module"].get_command_instance(
                self.domains[domain]["repository_factory"], context=context
            )
            cmd_wrapped = CommandWrapper(domain, cmd_instance)

            # Innermost layer to time and do method call
            cmd_wrapped.register_middleware(TimeFunctionCall())

            for middleware in self.command_wrapper_middleware:
                middleware_init = middleware(
                    self.infrastructure_factory, context=context
                )
                cmd_wrapped.register_middleware(middleware_init)

            # Outermost layer to manage infrastructure state
            cmd_wrapped.register_middleware(
                InfrastructureStateManager(
                    self.infrastructure_factory, context=context
                )
            )
        return cmd_wrapped
