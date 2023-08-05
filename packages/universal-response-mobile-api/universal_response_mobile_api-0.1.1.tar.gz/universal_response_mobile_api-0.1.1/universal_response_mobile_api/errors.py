import logging
from traceback import format_exc

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler
from rest_framework.response import Response

log = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    exc - объект исключения, например: <class 'django.core.exceptions.PermissionDenied'>
    context - бесполезен

    пример:
    http://localhost:8000/agent/salesplan/
    перехват <class 'django.core.exceptions.PermissionDenied'>

    http://localhost:8000/agent
    404 не перехватывает
    но http://localhost:8000/agent/salesplan/2000/
    404 перехватил

    В message можно отдать response.data, это может быть объект разного типа,
    там может быть подробное инфо об ошибке.
    Или exc.default_detail, это str с кратким описанием ошибки.
    Добавить в настройки:
    REST_FRAMEWORK = {
        ...
        'EXCEPTION_HANDLER': 'src.apps.common.errors.custom_exception_handler',
        ...
    }
    """
    response = exception_handler(exc, context)
    msg = _('Ошибка в запросе')
    status_code = 500

    try:
        if not hasattr(response, 'status_code'):
            # python exception:
            if isinstance(exc, ValidationError):
                msg = str(exc.messages[0])
            else:
                msg = str(exc)
            status_code = 500

        elif not hasattr(exc, 'detail'):
            msg = str(exc)
            status_code = response.status_code

        elif isinstance(exc.detail, ErrorDetail):  # auth
            msg = exc.detail
            status_code = response.status_code

        elif isinstance(exc.detail, list):
            msg = exc.detail[0]
            status_code = response.status_code

        else:
            for e in exc.detail.values():
                msg = e[0]
                break
            status_code = response.status_code
    except:
        log.error(format_exc())

    log.error(exc)

    structured_exc = {
        'success': False,
        'error': status_code,
        'message': msg,
        'response': None
    }
    return Response(structured_exc, status=status_code)
