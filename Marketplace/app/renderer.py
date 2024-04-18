from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, (ReturnDict, dict)):
            success = renderer_context['response'].status_code < 400
            status_code = renderer_context['response'].status_code
            message = data.pop('message', None)

            content = {
                'success': success,
                'message': message,
                'status_code': status_code,
                'data': data.pop('data', []),
                
            }
            error_message = data.pop('error_message', None)
            if error_message is not None:
                content['error_message'] = error_message
            
            total_cash = data.pop('total_cash', None)
            if total_cash is not None:
                content['total_cash'] = total_cash

            

            return super().render(content, accepted_media_type, renderer_context)

        elif isinstance(data, (ReturnList, list)):
            return super().render(data, accepted_media_type, renderer_context)

        else:
            return super().render(data, accepted_media_type, renderer_context)
