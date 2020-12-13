from http import HTTPStatus
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from requests import get as get_req

from api_server.settings import OMDB_API_TOKEN
from api_server.settings import OMDB_API_URL

def index(request):
    """Main function of the Movie API"""

    params = request.GET.dict()
    title = params.get('title')
    year = params.get('year')
    plot = params.get('plot')

    # Validating presense of necessary request parameters
    if (not title) or (not year) or (not plot):
        return HttpResponseBadRequest('At least 1 required parameter is missing')

    # Sending request to OMDb API endpoint
    # API reference: http://www.omdbapi.com/
    omdb_response = get_req(OMDB_API_URL, params={
        'apikey': OMDB_API_TOKEN, # API access token
        'r': 'json',              # Data type to return
        't': title,               # Movie title to search for
        'y': year,                # Year of release
        'p': plot                 # Return short or full plot
    })
    status = omdb_response.status_code

    # HTTP response status check
    if status != HTTPStatus.OK:
        response = HttpResponse('OMDb API error')
        response.status_code = status
        return response

    try:
        data = omdb_response.json()

        # This validation is required, because OMDb returns
        # status 200 when nothing is found
        if data.get('Response') == 'False':
            error_message = data.get('Error')

            if error_message == 'Movie not found!':
                return HttpResponseNotFound()
            elif error_message:
                return HttpResponseServerError(error_message)
            else:
                return HttpResponseServerError()
    except ValueError:
        return HttpResponseServerError('OMDb API returned invalid JSON')

    return JsonResponse(data)
