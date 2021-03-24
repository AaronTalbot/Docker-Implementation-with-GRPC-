from __future__ import print_function

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import random
import time


def make_message(message):
    return bidirectional_pb2.Message(
        message=message
    )


def generate_messages():
    print("BEFORE READ FILE")
    f = open("Client/r_dataisbeautiful_posts.csv", "r")
    index = 0
    print("DO I GET TO GENERATE MESSAGES")
    for line in f:
        if index != 0:
            msg = make_message(line)
            yield msg
        index = index + 1
        time.sleep(random.randint(1,10))



def send_message(stub):
    response = stub.GetServerResponse(generate_messages())
    print("There server has completed =  %s" % response.response)


def run():
    with grpc.insecure_channel('server:50051') as channel:
        print("DO I GET TO CLIENT RUN")
        stub = bidirectional_pb2_grpc.BidirectionalStub(channel)
        send_message(stub)

def read_file():
    print("DO I GET TO FILE GENERATE")
    return open("r_dataisbeautiful_posts.csv", "r")




if __name__ == '__main__':
    run()