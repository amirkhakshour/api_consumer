from collections import OrderedDict
from urllib.parse import urlsplit, urlunsplit


def _encode_nested_dict(key, data, fmt="%s[%s]"):
    d = OrderedDict()
    for sub_key, sub_value in data.items():
        d[fmt % (key, sub_key)] = sub_value
    return d


def encode_url_params(params):
    for key, value in params.items():
        if value is None:
            continue
        elif isinstance(value, list) or isinstance(value, tuple):
            for i, s_v in enumerate(value):
                if isinstance(s_v, dict):
                    sub_dict = _encode_nested_dict("%s[%d]" % (key, i), s_v)
                    for k, v in encode_url_params(sub_dict):
                        yield (k, v)
                else:
                    yield ("%s[%d]" % (key, i), s_v)
        elif isinstance(value, dict):
            sub_dict = _encode_nested_dict(key, value)
            for sub_key, sub_value in encode_url_params(sub_dict):
                yield (sub_key, sub_value)
        else:
            yield (key, value)


def build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))
