def filter_response_code(response_code):
    def filter_inner(log):
        return log.response_code == response_code
    return filter_inner


