from flask import Flask, json
from flask import request
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin


mysql = MySQL()
app = Flask(__name__)
CORS(app)
app.config['MYSQL_DATABASE_USER'] = 'tpartner'
app.config['MYSQL_DATABASE_PASSWORD'] = 'coletividade!@#'
app.config['MYSQL_DATABASE_DB'] = 't-partner_survey-heavyweight'
app.config['MYSQL_DATABASE_HOST'] = 'surveys.nees.com.br'

mysql.init_app(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/saveSteps", methods = ['POST'])
def saveStep():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
    except Exception, e:
        print e,'\nFail on trying to connect to database.'
        return e
    finally:
        pass


    try:
        json = request.json
        steps = json['answers']
    except Exception, e:
        print e,'\nFail on trying to get JSON data.'
        return e
    finally:
        pass


    try:
        index = 1
        for step in steps:
            query = "INSERT INTO steps_system (user_id,step,step_response) VALUES ('"+user_id+"',"+str[index]+",'"+str(step)+"');"
            print (query)
            cur.execute(query)
            index += 1

    except Exception, e:
        print e,'\nFail on trying to insert steps to database.'
        return e
    finally:
        pass

@app.route("/save", methods = ['POST'])
def save():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
    except Exception, e:
        print e,'\nFail on trying to connect to database.'
        return e
    finally:
        pass


    try:
        json = request.json
        answers = json['answers']
        user = json['user']
        steps = json['steps']
    except Exception, e:
        print e,'\nFail on trying to get JSON data.'
        return e
    finally:
        pass

    try:
        user_nationality = t(user['nationality'])
        query = "INSERT INTO users (gender,age,occupation,education_degree,nationality,language,agree_terms,system,how_long_work,employment_status,use_technology,computer_skills,formal_training,able_use) VALUES ('"+user['gender']+"','"+str(user['age'])+"','"+user['occupation']+"','"+user['education_level']+"','"+user_nationality+"','"+user['language']+"','"+str(user['agree_terms'])+"','"+json['system']+"','"+user['how_long_work']+"','"+user['employment_status']+"','"+user['use_technology']+"','"+user['skills']+"','"+user['trained']+"','"+user['able_use_technology']+"');"
        print (query)
        cur.execute(query)
        user_id = str(cur.lastrowid)
    except Exception, e:
        print e,'\nFail on trying to insert user to database.'
        return e
    finally:
            pass

    try:
        for step in answers:
            index = 1
            for answer in answers[step]:
                answer = t(answer)
                query = "INSERT INTO answers (text,question_id,user_id,step) VALUES ('"+str(answer)+"','"+str(index)+"','"+user_id+"','"+step+"');"
                print (query)
                cur.execute(query)
                index += 1
    except Exception, e:
        print e,'\nFail on trying to insert answers to database.'
        return e
    finally:
        pass

    try:
        query = "INSERT INTO logs (user_id,page,time) VALUES ('"+user_id+"','all_steps','"+str(json['global_time'])+"');"
        print (query)
        cur.execute(query)
        index = 1
        for time in json['step_time']:
            query = "INSERT INTO logs (user_id,page,time) VALUES ('"+user_id+"','"+str(index)+"','"+str(time)+"');"
            print (query)
            cur.execute(query)
            index+=1
    except Exception, e:
        print e,'\nFail on trying to insert logs to database.'
        return e
    finally:
        pass

    try:
        for step in steps:
            ui = str(user_id)
            st = str(step)
            sd = t(steps[step])
            query = "INSERT INTO steps_system (user_id,step,step_response) VALUES (%s,%s,%s);"
            print (query) % (ui,st,sd)
            cur.execute(query,(ui,st,sd))

    except Exception, e:
        print e,'\nFail on trying to insert steps to database.'
        return e
    finally:
        pass

    try:
        conn.commit()
    except Exception, e:
        print e,'\nFail on trying to commit to database.'
        return e
    finally:
        pass

    return "200 OK"

def t(string):
    if isinstance(string, basestring):
        newstring = []
        for i in range(0, len(string)):
            if not is_ascii(string[i]) or string[i]=='\'':
                newstring.append('#')
            else:
                    newstring.append(string[i])
        string = ''.join(newstring)
    return string

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

if __name__ == "__main__":
        app.run(host='::',port=5002,debug=True)
