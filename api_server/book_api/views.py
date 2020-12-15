from http import HTTPStatus
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.views import View
from requests import get as get_req

from api_server.settings import OPENLIB_ISBN_API_URL

class BookJSONView(View):
    """
    This class handles book request handling and view representation.
    """

    def get(self, request):
        """
        Main GET request handler. Requires 1 parameter of a book: ISBN (`isbn`).
        For more info on ISBN, see wiki: https://en.wikipedia.org/wiki/International_Standard_Book_Number.
        """

        # Validating presense of necessary request parameter
        isbn = request.GET.dict().get("isbn")
        if not isbn:
            return HttpResponseBadRequest("No \"isbn\" parameter found")

        # Sending request to OpenLibrary API endpoint
        # API reference: https://openlibrary.org/dev/docs/api/books
        openlib_url_query = self.create_openlib_url_query(isbn)
        openlib_response  = get_req(openlib_url_query)

        # HTTP response status check
        status = openlib_response.status_code
        if status != HTTPStatus.OK:
            response             = HttpResponse('OpenLibrary API error')
            response.status_code = status
            return response

        data = self.parse_response_json(openlib_response)

        return self.select_response(data)

    def create_openlib_url_query(self, isbn):
        """
        Forms URL query string for OpenLibrary API from ISBN
        """

        url_path = f'{isbn}.json'
        if not OPENLIB_ISBN_API_URL.endswith('/'):
            url_path = f'/{url_path}'
        
        return f"{OPENLIB_ISBN_API_URL}{url_path}"

    def parse_response_json(self, response):
        """
        Returns parsed JSON of the response if successful, if not - None
        """

        try:
            return response.json() # Parsing received JSON
        except ValueError:
            return None

    def select_response(self, data):
        """
        Returns a proper response relying on API response data
        """

        if data:
            return JsonResponse(data)
        else:
            return HttpResponseServerError('OpenLibrary API returned invalid JSON')