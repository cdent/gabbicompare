
from six.moves.urllib import parse as urlparse

from gabbi.handlers import base
from gabbi.handlers import jsonhandler
from gabbi import utils


class CompareHandler(base.ResponseHandler):
    """A ResponseHandler to compare JSON reponses.

    A ``source`` in ``response_compare`` is compared with the JSON
    returned from the target URL in the test.
    """

    test_key_suffix = 'compare'
    test_key_value = {}

    def __init__(self):
        super(CompareHandler, self).__init__()
        self.json = jsonhandler.JSONHandler()

    def __call__(self, test):
        """Implement our own to make the HTTP call."""
        if test.test_data[self._key] and len(test.test_data[self._key].get('paths')):
            self.preprocess(test)
            if not isinstance(
                    test.test_data[self._key], type(self.test_key_value)):
                raise GabbiFormatError(
                    "%s in '%s' has incorrect type, must be %s"
                    % (self._key, test.test_data['name'],
                       type(self.test_key_value)))
            # This is our additions.
            paths = test.test_data[self._key]['paths']
            source = test.test_data[self._key]['source']
            parsed_source = urlparse.urlsplit(source)
            parsed_url = urlparse.urlsplit(test.url)
            headers = test.test_data['request_headers']
            # Replace the test target url's scheme and netloc with the source.
            full_url = urlparse.urlunsplit((
                parsed_source.scheme, parsed_source.netloc, parsed_url.path,
                parsed_url.query, ''))
            if test.test_data['data'] != '':
                body = test._test_data_to_string(
                    test.test_data['data'],
                    utils.extract_content_type(headers, default='')[0])
            else:
                body = ''
            response, content = test.http.request(
                full_url,
                method=test.test_data['method'].upper(),
                headers=headers,
                body=body,
                redirect=test.test_data['redirects']
            )
            data = self.json.loads(content)
            for path in paths:
                path = test.replace_template(path)
                source_match = self.json.extract_json_path_value(data, path)
                target_match = self.json.extract_json_path_value(test.response_data, path)
                test.assertEqual(source_match, target_match,
                        "Expecting %s, got %s" % (source_match, target_match))

    def action(self, test, path, value=None):
        pass
