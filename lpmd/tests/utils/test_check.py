"""pytest for lpmd.utils.check."""
import pytest

import lpmd.utils.check as check

test_url = {
    "effective": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032117924&fileKind=0",
    "ineffective": "http://xxxxxx/dummy/test/xxxxxx.jp",
    "raise_str": 123456789,
    "raise_protocol": "ftp://xxxxxxxxxxxxxxxxxxxxxx",
}


class TestCheck:
    """pytest for lpmd.utils.check."""

    @pytest.mark.parametrize(
        "url, exp",
        [
            (test_url["effective"], True),
            (test_url["ineffective"], False),
        ],
    )
    def test_check_url(self, url, exp):
        """Unit test for check_url."""
        tgt = check.check_url(url)
        assert tgt == exp

    def test_raise_str_check_url(self):
        """Raise test for check_url on whether specified url is str."""
        msg = "Specified url must be str."
        with pytest.raises(TypeError, match=msg):
            check.check_url(test_url["raise_str"])

    def test_raise_protocol_check_url(self):
        """Raise test for check_url on whether specified url starts with http:// or https://."""
        msg = "Specified url must start with `http://` or `https://`."
        with pytest.raises(ValueError, match=msg):
            check.check_url(test_url["raise_protocol"])
