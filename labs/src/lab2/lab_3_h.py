from labs.src.lab2.filter_func import filter_lines


def filter_by_domain(*domains):

    def filter(log):
        return any(log.hostname.lower().endswith('.' + domain) for
                   domain in domains)

    return filter_lines(filter)


if __name__ == '__main__':
    filter_by_domain('pl')