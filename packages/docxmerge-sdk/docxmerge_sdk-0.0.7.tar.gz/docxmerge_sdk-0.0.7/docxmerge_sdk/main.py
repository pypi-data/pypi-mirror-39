import json
import os
import tempfile
from shutil import copyfile

import docxmerge_sdk.swagger_client as swagger


class Docxmerge:
    def __init__(self, apikey=""):
        configuration = swagger.configuration.Configuration()
        if apikey != "":
            configuration.api_key = {
                'ApiKey': apikey
            }
        configuration.host = "https://api.docxmerge.com"
        api_client = swagger.ApiClient(configuration)
        if apikey != "":
            api_client.default_headers = {'ApiKey': apikey}

        self.api_templates = swagger.TemplatesApi(api_client=api_client)
        self.api_api = swagger.ApiApi(api_client=api_client)

    def get_templates(self, tenant, page, size):
        return self.api_templates.api_by_tenant_templates_get(tenant, page=page, size=size)

    def render_file(self, document, data={}):
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(json.dumps(data).encode('utf-8'))
            fp.flush()
            return self.api_api.api_print_post(document.name, fp.name)

    def merge_template(self, tenant, document, data={}):
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(json.dumps(data).encode('utf-8'))
            fp.flush()
            return self.api_templates.api_by_tenant_merge_post(tenant, document.name, fp.name)


def temp_opener(name, flag, mode=0o777):
    return os.open(name, flag | os.O_TMPFILE, mode)
