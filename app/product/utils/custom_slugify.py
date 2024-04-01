import unicodedata
from django.utils.text import slugify
from transliterate import translit



def custom_az_slugify(value):
    value = unicodedata.normalize('NFKC', value)
    value = value.replace('ə', 'e')
    value = value.replace('ı', 'i')
    value = value.replace('ç', 'c')
    value = value.replace('ğ', 'g')
    value = value.replace('ş', 's')
    value = value.replace('ü', 'u')
    value = value.replace('ö', 'o')
    transliterated_text = translit(value, 'ru', reversed=True)
    return slugify(transliterated_text)

