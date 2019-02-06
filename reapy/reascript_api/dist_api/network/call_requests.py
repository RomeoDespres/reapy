import json

def decode_request(request):
    request = json.loads(request.decode("ascii"))
    return request

def decode_result(result):
    decoded_result = json.loads(result.decode("ascii"))
    for i, r in enumerate(decoded_result):
        if r["type"] == "error":
            raise_error(r["value"])
        else:
            decoded_result[i] = r["value"]
    return decoded_result
    
def encode_error(error):
    error_name = error.__class__.__name__
    args = error.args
    error = {"name": error_name, "args": args}
    return error

def encode_request(names, args):
    request = [{"name": n, "args": a} for n, a in zip(names, args)]
    request = json.dumps(request).encode("ascii")
    return request
    
def encode_result(result):
    encoded_result = result.copy()
    for i, r in enumerate(result):
        if isinstance(r, Exception):
            encoded_result[i] = {
                "type": "error",
                "value": encode_error(r)
            }
        else:
            encoded_result[i] = {
                "type": "result",
                "value": r
            }
    encoded_result = json.dumps(encoded_result).encode("ascii")
    return encoded_result
    
def raise_error(error):
    try:
        raise eval(error["name"])(*error["args"])
    except NameError as e:
        if error["name"] == "NameError":
            raise e
        raise Exception(error["name"], *error["args"])
