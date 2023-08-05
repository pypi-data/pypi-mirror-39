import bgdata
import re


class BgDataInterpolation(object):
    """
    This class will replace values following this schema:

        %(bgdata://project/dataset/version?build)

    with the bgdata path of the given data package
    """

    # compiled regexp to use in self.interpolate()
    _KEYCRE_PKG = re.compile(r"%\(bgdata://([^)]*)\)")
    _COOKIE_PKG = '%'

    # compiled regexp to find variables
    _KEYCRE_VAR = re.compile(r"\${([^}]*)}")
    _COOKIE_VAR = '${'

    def __init__(self, section):
        # the Section instance that "owns" this engine
        self.section = section

    def interpolate(self, key, value):

        # Replace variables
        if self._COOKIE_VAR in value:
            match = self._KEYCRE_VAR.search(value)
            while match:
                var_key = match.group(1)
                start, end = match.span()
                content = self.section.get(var_key, self.section.get('DEFAULT', {}).get(var_key, "${"+var_key+"}"))
                value = value[:start] + content + value[end:]

                match = self._KEYCRE_VAR.search(value, start + len(content))

        # Resolve bgdata packages
        if self._COOKIE_PKG not in value:
            return value

        match = self._KEYCRE_PKG.search(value)
        while match:
            start, end = match.span()
            path = bgdata.get(match.group(1))

            value = value[:start] + path + value[end:]
            match = self._KEYCRE_PKG.search(value, start + len(path))

        return value
