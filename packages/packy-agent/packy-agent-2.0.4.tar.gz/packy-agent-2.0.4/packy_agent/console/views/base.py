from urllib.parse import urlencode

import flask


def smart_redirect(endpoint, back_endpoint, button_text='Back'):
    back = urlencode({
        'back_url': flask.url_for(back_endpoint),
        'button_text': button_text,
    })
    url = flask.url_for(endpoint) + '?' + back
    return flask.redirect(url)
