from dis import dis
from io import StringIO
from nameko.web.handlers import http

"""
@api get /introspective
description: A route that looks inside itself
tags:
    - introspective
responses:
    '200':
        description: The disassembled contents of this route
    '404':
        description: A generic 404 page
"""


class IntrospectiveService:
    name = "introspective_service"

    @http('GET', '/introspective')
    def do_a_thing(self, _):
        with StringIO() as output:
            dis(self.do_a_thing, file=output)
            return str(output.getvalue())

"""
@api post /hotdog
description: A route for ordering a hotdog
tags:
    - hotdog
responses:
    '200':
        description: A message confirming your order
    '404':
        A generic 404 page
    '451':
        You are unable to order a hotdog for legal reasons
"""

class HotdogService:
    name = "hotdog_service"

    @http('POST', '/hotdog')
    def order_a_hotdog(self, _):
        return "One hotdog, comin' up!"

