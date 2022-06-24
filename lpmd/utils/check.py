"""lpmd.utils.check."""


def check_url(url):
    """Check whether specified url is effective.

    Parameters
    ----------
    url : str
        URL.

    Returns
    -------
    is_effective : bool
        if specified url is effective, True; otherwise False.

    """
    url_protocol = ["http://", "https://"]
    is_effective = True
    if not isinstance(url, str):
        msg = "Specified url must be str."
        raise TypeError(msg)
    else:
        include_protocol = [url.startswith(protocol) for protocol in url_protocol]
        if not any(include_protocol):
            msg = "Specified url must start with `http://` or `https://`."
            raise ValueError(msg)

        import urllib.error
        import urllib.request

        try:
            session = urllib.request.urlopen(url)
            session.close()
        except urllib.error.URLError:
            is_effective = False

    return is_effective
