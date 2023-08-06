import yaml


def dump_all_routes(api):
    result = api.routes.list()
    body = result.body

    updated = {
        'version': 1,
        'data': body['data'],
    }

    return yaml.dump(updated)


def sync_all_routes(api, dump_data, route_process_listener=None):
    return __write_routes(dump_data, route_process_listener, lambda route_id, payload: api.routes.update(route_id, body=payload))


def create_all_routes(api, dump_data, route_process_listener=None):
    return __write_routes(dump_data, route_process_listener, lambda route_id, payload: api.routes.create(route_id, body=payload))


def __write_routes(dump_data, route_process_listener, api_call_function):
    payloads = yaml.load(dump_data)
    results = []
    for route in payloads['data']:
        route_id = route['id']
        payload = {'data': route}
        result = api_call_function(route_id, payload)
        if route_process_listener:
            route_process_listener(route_id)
        results.append(result.body['data'])

    updated = {
        'version': 1,
        'data': results,
    }

    return yaml.dump(updated)
