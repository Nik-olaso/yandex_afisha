from django.shortcuts import render, get_object_or_404
from .models import Place
from django.http import JsonResponse


def index(request):
    places = Place.objects.all()
    features = []
    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"/places/{place.id}/",
            }
        })

    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, 'index.html', context={'places': places_geojson})


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    all_images = place.images.all().order_by('position')
    image_urls = [img.image.url for img in all_images]

    response_data = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lat": place.lat,
            "lng": place.lng,
        }
    }

    return JsonResponse(
        response_data,
        json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )