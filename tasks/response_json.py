from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        resolver_match = renderer_context.get('request').resolver_match
        url_name = resolver_match.url_name if resolver_match else None

        response_data = {
            'message': None,
            'status': 'ok',
            'data': {
                url_name: data.get('results') if 'results' in data else data,
            },
        }

        # Check if pagination data is available
        if 'count' in data:
            paginator_data = {
                'count': data['count'],
                'next': data.get('next', None),
                'previous': data.get('previous', None),
            }

            if any(paginator_data.values()):
                response_data['paginator'] = paginator_data

        return super().render(response_data, accepted_media_type, renderer_context)
