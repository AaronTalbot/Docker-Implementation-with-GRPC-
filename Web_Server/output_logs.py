from flask import Flask
import redis
import logging
app = Flask(__name__)

@app.route('/')

def print_logs():
    output = ""

    ar = ["num_comments", "Cumilative","percentage_OC","max_score"]
    try:
        conn = redis.StrictRedis(host='redis', port=6379)
        for key in conn.scan_iter("log.greeter_server*"):
            st = str(key)
            st = st.strip("'")
            a = st.split(".")
            ky = str(a[-1])

            val = str(conn.get(key))
            val = val.strip("b")
            val = val.strip("'")

            if ky in ar:
                if ky==ar[0]:
                    output+="The most comments on a post is: " + val + "<br>"
                elif ky==ar[1]:
                    if val != "0":
                        output+="The rolling 3 minute metric for Average score of the last set of posts is : " + val+ "<br>"
                    else:
                        output+="The initial rolling 3 minute metric has not been computed yet"+ "<br>"
                elif ky==ar[2]:
                    output+= "The percenatge of Original Content [OC] is: " + val + "%"+ "<br>"
                else:
                    output+= "The max Score of a post is: " + val+ "<br>"

            # Percentage_OC = 0.0
            # LOG_INPUT = conn.get(key)
            # arr = str(LOG_INPUT).strip(",")
            # OC = arr[0]
            # Mac_comments = arr[1]
            # Max_Score = arr[2]
            # Rolling_Average = arr[3]
            # value = str(conn.get(key))
            # print(conn.get(key))
            # output+= str(key) + value + '<br>'
            # value = str(conn.get(key))
            # array = value.split(",")
            # OC = array[0]
            # Max_Comments = array[1]
            # # Max_Score = array[2]
            # output+= "THIS IS WHAT LOG INPUT = " + str(LOG_INPUT) +"<br>"
            # output+= "Percentage of Orginal Conent [OC]: "+ str(OC) + "<br>"
            # output+="The most comments on a post are :"+ str(Mac_comments) + "<br>"
            # output+= "Max Score on a post is: "+ str(Max_Score) + "<br>"
            # output+= "Rolling Metric = " + str(Rolling_Average) + "<br>"
            # output+= "THIS IS THE END OF THE LOOP <br>"
            # output+= "The maximum amount of comments are: "+Max_Comments+"<br>"
            # output+= "The max score for a post is: "+Max_Score+"<br>"
            # output+= "----------------------------------------------"+"<br>"
    except Exception as ex:
        output = 'Error: ' + str(ex)
    return output

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
    # ma_logger = logging.getLogger(__name__)

