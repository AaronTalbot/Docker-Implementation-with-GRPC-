from concurrent import futures

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import time
import redis
# line[0] = id
# line[1] = title
# line[2] = score
# line[3] = author
# line[4] = author_flair_text
# line[5] = removed_by
# line[6] = total_awards_recieved
# line[7] = awarders
# line[8] = created_utc
# line[9] = full_link
# line[10] = num_comments
# line[11] = over_18 (NSFW)



class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):

    def GetServerResponse(self, request_iterator, context):
        iterator = 0
        num_comments = 0
        Cumilitave_score = 0
        amount_of_reads = 0
        line_holder_comments = []
        Initial_time = time.time()
        max_score = 0
        line_holder_score = []
        start_time = time.time()
        lines_counted = 1
        amount_oc = 0
        percentage_OC = 0.0
        Average = 0
        for Messages in request_iterator:
            if iterator % 10 == 0:
                try:
                    conn = redis.StrictRedis(host='redis',port=6379)
                    conn.set("log.greeter_server.OC", str(percentage_OC))

                    conn.set("log.greeter_server.num_comments",str(num_comments))
                    conn.set("log.greeter_server.max_score", str(max_score))
                    conn.set("log.greeter_server.Cumilative", str(Average))
                except Exception as ex:
                    print("Redis Error: ",ex)
            line = read_line(Messages.message)
            num_comments = Compute_MaxComments(line, num_comments)
            max_score = Compute_MaxScore(line, max_score)
            Average, Cumilitave_score, amount_of_reads, start_time = AverageScoreOverTime(line, start_time, Cumilitave_score, amount_of_reads, Average)
            amount_oc, percentage_OC = percentage_Original(lines_counted,line,amount_oc)
            lines_counted+=1
            iterator+=1
        return bidirectional_pb2.Response(response = True)




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(BidirectionalService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def read_line(line_info):
    l = line_info.split(",")
    if len(l) > 12:
        diff = len(l) -12
        for i in range(diff):
            l[1] += "," + l[2]
            l.pop(2)
    return l

def percentage_Original(amount, line, amount_oc):
    OC = "[OC]"
    if OC in line[1]:
        amount_oc+=1


    if amount_oc > 0:
        per = (amount_oc/amount)*100
        return amount_oc,per
    else:
        return amount_oc,0




def Compute_MaxComments(line, num_comments):
    # print("Does it make it here? (Max Comments)")
    if int(line[10]) > num_comments:
        line_holder_comments = line
        num_comments = int(line[10])
    return num_comments
    

def Compute_MaxScore(line, max_score):
    # print("Does it make it here? (Max Score)")
    # print("line[2] = ", line[2])
    if int(line[2]) > max_score:
        line_holder_score = line
        max_score = int(line[2])
        # print("Max Score", max_score)
    return max_score
    


def AverageScoreOverTime(line, start_time, Cumilitave_score, amount_of_reads, Average):
    Current_Time = time.time()
    Arr = []
    if Current_Time - start_time >= 180:
        Average = Cumilitave_score / amount_of_reads
        start_time = time.time()
        Cumilitave_score = 0
        amount_of_reads = 0
        print("Average over the last 3 minutes is : " + str(Average))
    else:
        Cumilitave_score = Cumilitave_score + int(line[2])
        amount_of_reads += 1
    return  Average, Cumilitave_score, amount_of_reads, start_time
        


if __name__ == '__main__':
    serve()