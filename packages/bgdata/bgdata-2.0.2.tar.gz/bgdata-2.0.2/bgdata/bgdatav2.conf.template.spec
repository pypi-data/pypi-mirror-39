
version = integer(default=None)

local_repository = string(default='~/.bgdata')
remote_repository = string(default='https://bbglab.irbbarcelona.org/bgdata')
offline = boolean(default=False)

[cache_repositories]
    __many__ = string