import json

def decode_request(request):
    request = json.loads(request.decode("ascii"))
    function_name, args = request["function_name"], request["args"]
    return function_name, args

def decode_result(result):
    decoded_result = json.loads(result.decode("ascii"))
    if isinstance(decoded_result, dict) and "error_name" in decoded_result:
        handle_error(decoded_result)
    return decoded_result
    
def encode_error(error):
    error_name = error.__class__.__name__
    args = error.args
    error = {"error_name": error_name, "args": args}
    error = json.dumps(error).encode("utf-8")
    return error

def encode_request(function_name, args):
    request = {"function_name": function_name, "args": args}
    request = json.dumps(request).encode("ascii")
    return request
    
def encode_result(result):
    result = json.dumps(result).encode("ascii")
    return result
    
def handle_error(error):
    error_name, args = error["error_name"], error["args"]
    try:
        raise eval(error_name)(*args)
    except NameError as e:
        if error_name == "NameError":
            raise e
        raise Exception(error_name, *args)