from flask import Flask
import redis

app = Flask(__name__)

@app.route('/')

def print_logs():
    output = ""
    try:
        conn = redis.StrictRedis(host='redis', port=6379)
        for key in conn.scan_iter("log.greeter_server*"):
            Percentage_OC = 0.0
            if(conn.get(key) == "percentage_OC"):
                Percentage_OC = conn.get(key)
            # value = str(conn.get(key))
            # print(conn.get(key))
            # output+= str(key) + value + '<br>'
            # value = str(conn.get(key))
            # array = value.split(",")
            # OC = array[0]
            # Max_Comments = array[1]
            # Max_Score = array[2]
            output+= "Percentage of Orginal Conent [OC]: "+ str(Percentage_OC) + "<br>"
            # output+= "The maximum amount of comments are: "+Max_Comments+"<br>"
            # output+= "The max score for a post is: "+Max_Score+"<br>"
            # output+= "----------------------------------------------"+"<br>"
    except Exception as ex:
        output = 'Error: ' + str(ex)
    return output

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')