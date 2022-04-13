from base64 import decode
from flask import Flask, request, jsonify, redirect
import sys, json, traceback
import data_collection
import model_manager

# Initialize flask application
app = Flask(__name__)

try_use_device = 'gpu' if 'gpu' in sys.argv else 'cpu'

model_manager.tf_init(try_use_device)
print(f"""
    ######################################
    ## Tensorflow is utilizing the {try_use_device}! ##
    ######################################
""")


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    
    try:
        if request.method == "GET":
            return """
            <h1>Model Endpoint For InceptionTime - (MEFIT)</h1>
            <p>Use this api by making post requests to this endpoint.</p>
            <hr>
            <code>curl -X POST -H 'Content-Type:application/json' http://172.28.198.13:5000/predict -d '{"id":"tester", "content":[-193, 38, -183, -50, 44, 8]}'</code>
            <p>or (if local instance):</p>
            <code>curl -X POST -H 'Content-Type:application/json' http://localhost:5000/predict -d '{"id":"tester", "content":[0, 38, 183, 950, 494, 0]}'</code>
            <hr>
            <p>ps. if you dont know how to make post requests, click <a href="https://www.w3schools.com/python/ref_requests_post.asp">here</a>.</p>
            """

        # get request json object
        post_data = request.get_json()
        print(post_data)

        # extract vars from post json
        input_arr = post_data['content']

        prediction = model_manager.predict_from_array(input_arr)
         
        # create json response object
        response_json = {
            'class1': json.dumps(prediction[0, 0].item()),
            'class2': json.dumps(prediction[0, 1].item())
            }

        if not max(response_json) == 'class1':
            brpower = int(sum([float(x) for x in response_json.values()]) * 100)
            data_collector.alerter.gobrrr(pid=post_data['id'], power=brpower)
        print(brpower, response_json, max(response_json))

        # convert to response json object
        response = jsonify(response_json)
        response.status_code = 200
        return response
    except ValueError as e:
        print(e)
        response = jsonify({
            'message': 'Wrong length of array, format: {\"content\":[0.0, 38, 183, 200, 494, 0]}',
            'exception': str(type(e)) 
            })
        response.status_code = 400
        return response
    except Exception as e:
        print(e)
        response = jsonify({
            'message': 'Some error idk. format: {\"content\":[0.0, 38, 183, 200, 494, 0]\}',
            'exception': str(type(e)) 
            })
        response.status_code = 400
        return response
    

@app.route("/", methods=["GET"])
def health():
    if request.method == "GET":
        return "Working Fine"

@app.route("/ping", methods=["GET"])
def pingpong():
    if request.method == "GET":
        data_collector.alerter.gobrrr(custom_msg='Pong!')
        return "Ping!"

global_str = ''
@app.route("/update", methods=["GET", "POST"])
def update_model():
    global global_str
    if request.method == 'GET':
        datentime, hours_since = model_manager.get_last_model_renew_time()
        return f"""
        <h2>Last git model pull was at:</h2> 
        <h3>{datentime}</h3>
        <h3>Hours since last update: {hours_since}</h3>
        <hr>
        <form action="/update" method="post">
        <div><input type="submit" name="model" value="update">{global_str}</div>
        </form>
        """
    
    elif request.method == 'POST':
        if "model" in request.form:
            status_msg = model_manager.retrieve_new_model()
            global_str = ' <== Last update status recieved: ' + status_msg
            return redirect("update", code=303)
    else:
        return 'eh.. error i guess... how the fuck did you get here???'


@app.route("/test", methods=["GET", "POST"])
def prediction_interface():
    try:
        response = ''
        if request.method == "POST":
            post_data = request.form['content']
            
            float_input_arr = post_data.split(',')
            if not len(float_input_arr) > 1:
                float_input_arr = float_input_arr[0].split(' ')
            if not len(float_input_arr) > 1:
                float_input_arr = float_input_arr[0].split('\t')

        
            float_input_arr = filter(lambda x: x != "", float_input_arr)
            float_input_arr = list([float(i) for i in float_input_arr])

            response = float_input_arr
            prediction = model_manager.predict_from_array(float_input_arr)
            response = {
                'class1': json.dumps(prediction[0, 0].item()),
                'class2': json.dumps(prediction[0, 1].item())
            }
    except Exception as e:
        response = str(e)
    
    finally:
        return f"""
            <h3>Testing interface</h3>
            <p>Array should be comma OR space seperated OR tabs.</p>
            <hr>
            <form action="/test" method="post">
            <input style="width: 100px;" type="text" id="content" name="content">
            <br>
            <div><input type="submit" name="submit" value="submit"></div>
            </form>
            <code>{response}</code>
            """


@app.route("/collection", methods=["GET", "POST"])
def data_collection_interface():
    try:
        response = ''
        if request.method == "POST":
            print(request)
            post_data = request.get_json() or request.form   
 
            if isinstance(post_data['content'], str):
                float_input_arr = post_data['content'].split(',')
                if not len(float_input_arr) > 1:
                    float_input_arr = float_input_arr[0].split(' ')
                if not len(float_input_arr) > 1:
                    float_input_arr = float_input_arr[0].split('\t')
                float_input_arr = filter(lambda x: x != "", float_input_arr)
                float_input_arr = list([float(i) for i in float_input_arr])
            else:
                float_input_arr = post_data['content']

            user_id = post_data['id'] if 'id' in post_data else None
            user_id = user_id or 123
            datapoint_class = post_data['class'] if 'class' in post_data else None
            datapoint_class = datapoint_class or 1
            
            in_dict = {
                'id': user_id,
                'content': float_input_arr,
                'class': datapoint_class
            }

            data_collector.death_and_taxes(in_dict)

            response = f"Data collected from user; {user_id} with the class; {datapoint_class} and value; {float_input_arr}"
    except Exception as e:
        print(traceback.format_exc(), e)
        response = 'err:  '+str(e)
    
    finally:
        res_log = data_collector.simple_log(response)
        res_log = '<pre>'+'\n'.join(res_log)+'</pre>'
        return f"""
            <h3>Data Collection Interface - DCI</h3>
            <p>Data can be posted to this endpoint with below format</p>
            <p>Array should be comma OR space OR tab seperated.</p>
            <hr>
            <form action="/collection" method="post">
            <a>pid </a><input style="width: 100px;" type="text" id="pid" name="pid">
            <a>content </a><input style="width: 100px;" type="text" id="content" name="content">
            <a>class </a><input style="width: 100px;" type="text" id="class" name="class">
            <br>
            <div><input type="submit" name="submit" value="submit"></div>
            </form>
            <code>{res_log}</code>
            <script>
                function autoRefresh() {{
                    window.location = window.location.href;
                }}
                setInterval('autoRefresh()', 5000);
            </script>
            """


"""# only used for testing, could be removed. No dependents
def predict_testing():
    #inpu = [41, -345, -112, -383, -1223, 49]
    inpu = [-193, 38, -183, -50, 44, 8]

    item = array_to_prediction_obj(inpu)
    print('item =', item)
    prediction = model.predict(item)
         
    # create json response object
    response_json = {
        'class1': json.dumps(prediction[0, 0].item()),
        'class2': json.dumps(prediction[0, 1].item())
        }
    print(response_json)"""


if __name__ == "__main__":
    # run flask application in debug mode
    #predict_testing()
    data_collector = data_collection.TheCollector()
    app.run(debug=True, host="0.0.0.0", port=5000)
