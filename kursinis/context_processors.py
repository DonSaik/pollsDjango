from django.conf import settings # import the settings file


def language_code(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'LANGUAGE_CODE': request.LANGUAGE_CODE}


def language_url(request):
    if request.LANGUAGE_CODE == 'lt':
        return {
            'language_url':
            ""+(request.get_full_path().split('/lt', 2)[1])
        }
    else:
        return {
            'language_url':
                "/lt"+(request.get_full_path())
        }