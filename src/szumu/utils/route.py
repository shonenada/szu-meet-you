
route_list = []


def route(url_rule):
    def handler(handle_class):
        def decoration():
            new_rule = (url_rule, handle_class)
            self.route_list.append(new_rule)
        return decoration
    return handler
    