from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings
from importlib import import_module

class HealthViewSet(viewsets.ViewSet):
    """
    Health Checks
    """

    def __call_from_string(self, method_to_call):
        bits = method_to_call.split('.')
        method_name = bits.pop()
        module_name = (".").join(bits)

        module = import_module(module_name)
        func = getattr(module, method_name)
        return func()

    def list(self, request):

        data = {
            "status": "OK",
            "checks": []
        }
        for check in settings.HEALTH_CHECKS:
            data.get("checks").append(
                self.__call_from_string(check)
            )
        return Response(data)

    def retrieve(self, request, pk=None):
        """
        Run a specific test
        """
        result = {}
        method_name = pk.replace('-', '.')
        for check in settings.HEALTH_CHECKS:
            if check == method_name:
                result = self.__call_from_string(method_name)
                return Response(result)

        return Response("No healthcheck found", status=404)