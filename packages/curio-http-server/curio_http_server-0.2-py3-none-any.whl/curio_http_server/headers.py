from base64 import standard_b64decode
from email.utils import parsedate_to_datetime
from multidict import CIMultiDict
from ua_parser import user_agent_parser


class AuthorizationHeader(object):
    __slots__ = 'type', 'credentials', 'username', 'password', 'token'

    @classmethod
    def _from_value(cls, value):
        if value:
            if ' ' in value:
                type, credentials = value.split(' ', 1)

                return cls(type, credentials, value)

        return None

    def __init__(self, type, credentials, value):
        self.type = type
        self.credentials = credentials
        self.value = value

        if self.type == 'basic':
            try:
                userinfo = standard_b64decode(self.credentials)
                self.username, self.password = userinfo.split(':', 1)
            except:
                pass
        elif self.type == 'bearer':
            self.token = self.credentials


class ContentDispositionHeader(object):
    __slots__ = 'type', 'params', 'value'

    def __init__(self, type, params, value):
        self.type = type
        self.params = params
        self.value = value

    def __str__(self):
        return self.value

class ContentTypeHeader(object):
    __slots__ = 'type', 'subtype', 'suffix', 'params', 'value'

    @classmethod
    def _from_value(cls, value):
        if value:
            if '/' in value:
                parts = value.split(';')
                type, subtype_suffix = parts[0].split('/', 1)

                if '+' in subtype_suffix:
                    subtype, suffix = subtype_suffix.split('+', 1)
                else:
                    subtype, suffix = subtype_suffix, ''

                params = {}

                for part in parts[1:]:
                    name, value = part.split('=')
                    params[name.strip().lower()] = value.strip()

                return ContentTypeHeader(type.strip().lower(), subtype.strip().lower(), suffix.strip().lower(), params, value)

        return None

    def __init__(self, type, subtype, suffix, params, value):
        self.type = type
        self.subtype = subtype
        self.suffix = suffix
        self.params = params
        self.value = value

    def __str__(self):
        return self.value


class _UserAgentBrowser(object):
    __slots__ = 'family', 'major', 'minor', 'patch'

    def __init__(self, family, major, minor, patch):
        self.family = family
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        if self.major:
            if self.minor:
                if self.patch:
                    return f'{self.family}/{self.major}.{self.minor}.{self.patch}'
                else:
                    return f'{self.family}/{self.major}.{self.minor}'
            else:
                return f'{self.family}/{self.major}'
        else:
            return self.family


class _UserAgentOperatingSystem(object):
    __slots__ = 'family', 'major', 'minor', 'patch', 'patch_minor'

    def __init__(self, family, major, minor, patch, patch_minor):
        self.family = family
        self.major = major
        self.minor = minor
        self.patch = patch
        self.patch_minor = patch_minor

    def __str__(self):
        if self.major:
            if self.minor:
                if self.patch:
                    if self.patch:
                        return f'{self.family}/{self.major}.{self.minor}.{self.patch}.{self.patch_minor}'
                    else:
                        return f'{self.family}/{self.major}.{self.minor}.{self.patch}'
                else:
                    return f'{self.family}/{self.major}.{self.minor}'
            else:
                return f'{self.family}/{self.major}'
        else:
            return self.family


class _UserAgentDevice(object):
    __slots__ = 'family', 'brand', 'model'

    def __init__(self, family, brand, model):
        self.family = family
        self.brand = brand
        self.model = model

    def __str__(self):
        if self.brand:
            if self.model:
                return f'{self.family}/{self.brand}.{self.model}'
            else:
                return f'{self.family}/{self.brand}'
        else:
            return self.family


class UserAgentHeader(object):
    __slots__ = 'browser', 'operating_system', 'device', 'value'

    @classmethod
    def _from_value(cls, value):
        if value:
            user_agent_data = user_agent_parser.Parse(value)

            return cls(
                _UserAgentBrowser(
                    user_agent_data['user_agent'].get('family'),
                    user_agent_data['user_agent'].get('major'),
                    user_agent_data['user_agent'].get('minor'),
                    user_agent_data['user_agent'].get('patch')
                ),
                _UserAgentOperatingSystem(
                    user_agent_data['os'].get('family'),
                    user_agent_data['os'].get('major'),
                    user_agent_data['os'].get('minor'),
                    user_agent_data['os'].get('patch'),
                    user_agent_data['os'].get('patch_minor')
                ),
                _UserAgentDevice(
                    user_agent_data['os'].get('family'),
                    user_agent_data['os'].get('brand'),
                    user_agent_data['os'].get('model')
                ),
                value)

        return None

    def __init__(self, browser, operating_system, device, value):
        self.browser = browser
        self.operating_system = operating_system
        self.device = device
        self.value = value

    def __str__(self):
        return self.value


class BaseHeaders(CIMultiDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_disposition = None
        self.content_length = None
        self.content_md5 = None
        self.content_type = None
        self.date = None

    def _post_process(self):
        # TODO: Cache-Control
        # TODO: Connection
        # Content-Length
        content_length_value = self.get('Content-Length')

        if content_length_value:
            try:
                self.content_length = int(content_length_value)
            except ValueError:
                pass

        # Content-MD5
        content_md5_value = self.get('Content-MD5')

        if content_md5_value:
            try:
                self.content_md5 = standard_b64decode(content_md5_value)
            except:
                pass

        # Content-Type
        self.content_type = ContentTypeHeader._from_value(self.get('Content-Type'))
        # Date
        date_value = self.get('Date')

        if date_value:
            self.date = parsedate_to_datetime(date_value)

        # TODO: Pragma


class FormPartHeaders(BaseHeaders):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _post_process(self,):
        super()._post_process()
        # Content-Disposition
        content_disposition_value = self.get('Content-Disposition')

        if content_disposition_value:
            parts = content_disposition_value.split(';')
            params = {}

            for part in parts[1:]:
                name, value = part.split('=')
                params[name.strip().lower()] = value.strip()

            self.content_disposition = ContentDispositionHeader(parts[0].strip().lower(), params, content_disposition_value)


class RequestHeaders(BaseHeaders):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authorization = None
        self.user_agent = None

    def _post_process(self, request):
        super()._post_process()
        # TODO: A-IM
        # TODO: Accept
        # TODO: Accept-Charset
        # TODO: Accept-Datetime
        # TODO: Accept-Encoding
        # TODO: Accept-Language
        # TODO: Access-Control-Request-Headers
        # TODO: Access-Control-Request-Method
        # Authorization
        self.authorization = AuthorizationHeader._from_value(self.get('Authorization'))

        # Cookie
        cookie_value = self.get('Cookie')

        if cookie_value:
            parts = cookie_value.split(';')

            for part in parts:
                if '=' in part:
                    name, value = part.split('=', 1)
                    request.cookies[name.strip()] = value.strip()

        # TODO: Expect
        # TODO: Forwarded
        # TODO: From
        # Host
        host_value = self.get('Host')

        if host_value:
            self.host = host_value

            if ':' in host_value:
                host, port = host_value.split(':', 1)

                try:
                    request.port = int(port)
                    request.host = host
                except ValueError:
                    request.host = host_value
            else:
                request.host = host_value

        # TODO: HTTP2-Settings
        # TODO: If-Match
        # TODO: If-Modified-Since
        # TODO: If-None-Match
        # TODO: If-Range
        # TODO: If-Unmodified-Since
        # TODO: Max-Forwards
        # TODO: Origin
        # TODO: Proxy-Authorization
        # TODO: Range
        # TODO: Referer
        # TODO: TE
        # TODO: Upgrade
        # User-Agent
        self.user_agent = UserAgentHeader._from_value(self.get('User-Agent'))
        # TODO: Via
        # TODO: Warning


class ResponseHeaders(BaseHeaders):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _post_process(self, response):
        super()._post_process()
        # TODO: Accept-Patch
        # TODO: Accept-Ranges
        # TODO: Access-Control-Allow-Credentials
        # TODO: Access-Control-Allow-Headers
        # TODO: Access-Control-Allow-Methods
        # TODO: Access-Control-Allow-Origin
        # TODO: Access-Control-Expose-Headers
        # TODO: Access-Control-Max-Age
        # TODO: Age
        # TODO: Allow
        # TODO: Alt-Svc
        # TODO: Content-Disposition
        # TODO: Content-Encoding
        # TODO: Content-Language
        # TODO: Content-Length
        # TODO: Content-Location
        # TODO: Content-MD5
        # TODO: Content-Range
        # TODO: Content-Type
        # TODO: Delta-Base
        # TODO: ETag
        # TODO: Expires
        # TODO: IM
        # TODO: Last-Modified
        # TODO: Link
        # TODO: Location
        # TODO: P3P
        # TODO: Proxy-Authenticate
        # TODO: Public-Key-Pins
        # TODO: Retry-After
        # TODO: Server
        # TODO: Set-Cookie
        # TODO: Strict-Transport-Security
        # TODO: Tk
        # TODO: Trailer
        # TODO: Transfer-Encoding
        # TODO: Upgrade
        # TODO: Vary
        # TODO: Via
        # TODO: WWW-Authenticate
        # TODO: Warning
        # TODO: X-Frame-Options
