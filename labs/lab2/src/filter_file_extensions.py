def is_resource_of_type(*possible_extensions):

    def filter_inner(log):
        return any(log.resource_path.lower().endswith('.' + extension)
                   for extension in possible_extensions)
    return filter_inner


def is_host_of_domain(*domains):

    def filter_inner(log):
        return any(log.hostname.lower().endswith('.' + domain) for
                    domain in domains)
    return filter_inner
