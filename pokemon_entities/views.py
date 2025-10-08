import folium
from pokemon_entities.models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entitys = PokemonEntity.objects.filter(Disappeared_at__gte=localtime(), Appeared_at__lte=localtime())

    for pokemon_entity in pokemon_entitys:
        img_url = None
        if pokemon_entity.Pokemon.image:
            img_url = request.build_absolute_uri(pokemon_entity.Pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.Lat,
            pokemon_entity.Lon,
            img_url
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = None
        if pokemon.image:
            img_url = pokemon.image.url
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon_entitys = PokemonEntity.objects.filter(
        Pokemon=requested_pokemon,
        Disappeared_at__gte=localtime(),
        Appeared_at__lte=localtime()
        )

    pokemon = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
    }
    if requested_pokemon.previous_evolution:
        pokemon["previous_evolution"] = {
                "title_ru": requested_pokemon.previous_evolution.title_ru,
                "pokemon_id": requested_pokemon.previous_evolution.id,
                "img_url": requested_pokemon.previous_evolution.image.url,
                }
    if requested_pokemon.next_evolutions.filter().exists():
        pokemon["next_evolution"] = {
            "title_ru": requested_pokemon.next_evolutions.get().title_ru,
            "pokemon_id": requested_pokemon.next_evolutions.get().id,
            "img_url": requested_pokemon.next_evolutions.get().image.url,
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys:
        img_url = None
        if pokemon_entity.Pokemon.image:
            img_url = request.build_absolute_uri(pokemon_entity.Pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.Lat,
            pokemon_entity.Lon,
            img_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
