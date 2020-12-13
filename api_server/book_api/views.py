from http import HTTPStatus
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from requests import get as get_req

from api_server.settings import OPENLIB_ISBN_API_URL

def index(request):
    """Main function of the Book API"""

    # Validating presense of necessary request parameter
    isbn = request.GET.dict().get("isbn")
    if not isbn:
        return HttpResponseBadRequest("No \"isbn\" parameter found")

    # Forming URL query for OpenLibrary ISBN API
    openlib_url_query = "%s%s.json" % (OPENLIB_ISBN_API_URL, isbn)

    # Sending request to OpenLibrary ISBN API endpoint
    # API reference: https://openlibrary.org/dev/docs/api/books
    openlib_response = get_req(openlib_url_query)
    status = openlib_response.status_code

    # HTTP response status check
    if status != HTTPStatus.OK:
        response = HttpResponse("OpenLibrary ISBN API error")
        response.status_code = status
        return response

    try:
        data = openlib_response.json()
    except ValueError:
        return HttpResponseServerError("OpenLibrary ISBN API returned invalid JSON")

    return JsonResponse(data)
