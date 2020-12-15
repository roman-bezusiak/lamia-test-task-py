from http import HTTPStatus
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.views import View
from requests import get as get_req

from api_server.settings import OMDB_API_TOKEN
from api_server.settings import OMDB_API_URL

class MovieJSONView(View):
    """
    This class handles movie request handling and view representation.
    """

    def get(self, request):
        """
        Main GET request handler. Requires 3 parameters of a movie:
            1. Title (`title`)
            2. Year  (`year`)
            3. Plot  (`plot`)
        """

        title, year, plot, error_response = self.validate_request(request)
        if error_response:
            return error_response

        # Sending request to OMDb API endpoint
        # API reference: http://www.omdbapi.com/
        omdb_response = get_req(OMDB_API_URL, params={
            'apikey': OMDB_API_TOKEN, # API access token
            'r':      'json',         # Data type to return
            't':      title,          # Movie title to search for
            'y':      year,           # Year of release
            'p':      plot            # Return short or full plot
        })

        # HTTP response status check
        status = omdb_response.status_code
        if status != HTTPStatus.OK:
            response             = HttpResponse('OMDb API error')
            response.status_code = status
            return response

        data = self.parse_response_json(omdb_response)
        
        return self.select_response(data)

    def validate_request(self, request):
        """
        Validates incoming request. Returns request parameters and
        `error_response` in that exact order. On success only `error_response`
        is None, on failure - all the parameters are.
        """

        params = request.GET.dict()
        title  = params.get('title')
        year   = params.get('year')
        plot   = params.get('plot')

        if (not title) or (not year) or (not plot):
            return (
                None, None, None,
                HttpResponseBadRequest('At least 1 required parameter is missing')
            )
        else:
            return (title, year, plot, None)

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
            # Validating the response content. This is required, because
            # OMDb returns status 200 when nothing is found
            if data.get('Response') == 'False':
                error_message = data.get('Error')

                if error_message == 'Movie not found!':
                    return HttpResponseNotFound()
                elif error_message:
                    return HttpResponseServerError(error_message)
                else:
                    return HttpResponseServerError()

            return JsonResponse(data)
        else:
            return HttpResponseServerError('OpenLibrary API returned invalid JSON')