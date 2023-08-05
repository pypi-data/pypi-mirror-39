"""Error classes for bgdata"""


class BGDataError(Exception):
    """Base exception for this package"""
    pass


# Package
class PackageError(BGDataError):
    pass


class PackageNotFoundError(PackageError):
    pass


# Tag
class TagFileError(BGDataError):
    pass


class TagNotFound(BGDataError):
    pass


# Tag and info files
class RemoteFileError(BGDataError):
    pass


# Upload
class UploadError(BGDataError):
    pass


# Donwload
class DownloadError(BGDataError):
    pass
