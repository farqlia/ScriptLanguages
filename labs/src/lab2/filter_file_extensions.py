def filter_file_extensions(log, *possible_extensions):
    return any(log.resource_path.lower().endswith(extension)
                for extension in possible_extensions)


