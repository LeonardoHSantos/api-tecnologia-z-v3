from strategy.controllers.convert_data.convert import ConvertData


def prepare_msg(**kwargs):
    content = ConvertData.convert_to_dict(name=kwargs["name"], msg=kwargs["msg"], request_id=kwargs["request_id"])
    return ConvertData.convert_to_dumps(content)

# def prepare_msg_generic(**kwargs):
#     name = kwargs["name"]
#     msg = kwargs["content"]
#     request_id = kwargs["request_id"]
#     content = ConvertData.convert_to_dict(name=name, msg=msg, request_id=request_id)
#     return ConvertData.convert_to_dumps(content)