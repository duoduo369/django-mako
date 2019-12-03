# -*- coding: utf-8 -*-
from mako.lookup import TemplateLookup
import tempfile

class MakoMiddleware(object):

    def __init__(self, get_response):
        """Setup mako variables and lookup object"""
        self.get_response = get_response
        from django.conf import settings
        # Set all mako variables based on django settings
        global template_dirs, output_encoding, module_directory, encoding_errors
        TEMPLATE_DIRS = settings.TEMPLATES[0]['DIRS']
        directories      = getattr(settings, 'MAKO_TEMPLATE_DIRS', TEMPLATE_DIRS)
        module_directory = getattr(settings, 'MAKO_MODULE_DIR', tempfile.mkdtemp())
        output_encoding  = getattr(settings, 'MAKO_OUTPUT_ENCODING', 'utf-8')
        encoding_errors  = getattr(settings, 'MAKO_ENCODING_ERRORS', 'replace')

        global lookup
        lookup = TemplateLookup(directories=directories,
                                module_directory=module_directory,
                                output_encoding=output_encoding,
                                encoding_errors=encoding_errors,
                                )
        import djangomako
        djangomako.lookup = lookup

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
