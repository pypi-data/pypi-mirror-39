import grpc
import gateway_pb2
import gateway_pb2_grpc

__default_url = 'keti.asuscomm.com:32222'

def dcf(**kwargs):
    url = kwargs['url'] if 'url' in kwargs.keys() else __default_url
    service = kwargs['service'] if 'service' in kwargs.keys() else None
    arg = kwargs['arg'] if 'service' in kwargs.keys() else None
    
    if not (service and arg):
        raise Exception('DCF() takes at lest 2 arguments service and input. url is optional.')

    channel = grpc.insecure_channel(url)
    stub = gateway_pb2_grpc.GatewayStub(channel)
    servicerequest = gateway_pb2.InvokeServiceRequest(Service=service, Input=arg)
    r = stub.Invoke(servicerequest)
    return r.Msg

