def is_resource_of_type(log, *possible_extensions):
    return any(log.resource_path.lower().endswith('.' + extension)
               for extension in possible_extensions)


def is_host_of_domain(log, *domains):
    return any(log.hostname.lower().endswith('.' + domain) for
                domain in domains)
