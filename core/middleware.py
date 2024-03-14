from django.utils.deprecation import MiddlewareMixin


class AddVersionToStaticMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 200 and response['Content-Type'].startswith('text/html'):
            content = response.content.decode('utf-8')
            new_content = self._append_version_to_scripts(content)
            response.content = new_content.encode('utf-8')
        return response

    def _append_version_to_scripts(self, content):
        return content.replace('src="/static/', 'src="/static/?v1')