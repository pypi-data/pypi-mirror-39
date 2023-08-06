"""
author: arun.rs
13th November 2018
"""

class DependencyInjection(object):
    """
    This class is used for sharing objects across the application.
    objects which are registered in this object will be shared across
    all the instances of this class
    """

    # All the services are stored in this class variable and available to all
    # the instances of di object
    services = {}

    def set(self, service_name, service_object):
        """
        :summary: This method will register the services in class variable
        @param service_name: Name for the service to register in DI. Supposed to be
                            unique for each service registered.
        :param service_object: The service object which needs to be registered.
        :return: Returns 1 if there is no service is already registered in the same given name,
        Else store the given service_object for the service_name and return 0.
        :rtype: int
        """
        # If a service is already registered in the same name, store in a variable or store in None.
        existing_value_in_service = DependencyInjection.services.get(service_name, None)
        DependencyInjection.services[service_name] = service_object
        # If already a service was registered in the same name return 0 else return 1
        if (existing_value_in_service):
            return 0
        else:
            return 1

    def get(self, service_name):
        """
        :summary: Retrieves the requested service and returns it.
        :param service_name: service name for which the objects need
        to be returned
        :raise ServiceNotFoundException: raised when the given service_name
        is not found in services
        """
        if DependencyInjection.services.get(service_name):
            return DependencyInjection.services.get(service_name)
        else:
            raise Exception("ServiceNotFound : " + service_name)