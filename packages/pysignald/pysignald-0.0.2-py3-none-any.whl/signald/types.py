import attr


@attr.s
class Attachment:
    content_type = attr.ib(type=str)
    id = attr.ib(type=str)
    size = attr.ib(type=int)
    stored_filename = attr.ib(type=str)


@attr.s
class Message:
    username = attr.ib(type=str)
    source = attr.ib(type=str)
    message = attr.ib(type=str)
    source_device = attr.ib(type=int, default=0)
    timestamp = attr.ib(type=int, default=None)
    timestamp_iso = attr.ib(type=str, default=None)
    expiration_secs = attr.ib(type=int, default=0)
    attachments = attr.ib(type=list, default=[])
    quote = attr.ib(type=str, default=None)
