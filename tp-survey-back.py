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

def connectDatabase():
    try:
        conn = mysql.connect()
        
        return conn
    except Exception, e:
        print e,'\nFail on trying to connect to database.'
        return e
    finally:
        pass

    
def commit(conn):
    try:
        conn.commit()
    except Exception, e:
        print e,'\nFail on trying to commit to database.'
        return e
    finally:
        pass

def getResponse(request):
    try:
        json = request.json
        return json
    except Exception, e:
        print e,'\nFail on trying to get JSON data.'
        return e
    finally:
        pass

def savetime(cur,time,id_tela,user_id):
    try:
        query = "INSERT INTO logs (user_id,page,time) VALUES (%s,%s,%s)"
        cur.execute(query,(user_id,id_tela,time))

    except Exception, e:
        print e

def updateTime(cur,time,id_tela,user_id):
    try:
        query = "UPDATE logs SET time = %s WHERE user_id = %s AND page = %s"
        cur.execute(query,(time,user_id,id_tela))

    except Exception, e:
        print e
    
def normalizeUser(user):
        if 'highestLevel' not in user:
            user['highestLevel'] = ''
        if 'howLong' not in user:
            user['howLong'] = ''
        if 'howLong' not in user:
            user['how_long_work'] = ''
        if 'employmentStatus_Other' not in user:
            user['employmentStatus_Other'] = ''
        if 'employmentStatus' not in user:
            user['employmentStatus'] = ''
        if 'useTechnology' not in user:
            user['useTechnology'] = ''
        if 'skills' not in user:
            user['skills'] = ''
        if 'profileTreinament' not in user:
            user['profileTreinament'] = ''
        if 'ableuseTechnology' not in user:
            user['ableuseTechnology'] = ''

        return user

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/profile",methods = ['POST'])
def createProfile():
    conn = connectDatabase()
    cur = conn.cursor()
    json = getResponse(request)
   
    try:
        user = json['data']
        user_nationality = t(user['nationality'])
        user = normalizeUser(user);
        
        query = "INSERT INTO users (gender,age,occupation,education_degree,nationality,language,agree_terms,system,how_long_work,employment_status,use_technology,computer_skills,formal_training,able_use) VALUES ('"+user['gender']+"','"+str(user['age'])+"','"+user['occupation']+"','"+user['highestLevel']+"','"+user_nationality+"','"+user['language']+"','"+str(user['agree_terms'])+"','"+user['system']+"','"+user['howLong']+"','"+user['employmentStatus']+"','"+user['useTechnology']+"','"+user['skills']+"','"+user['profileTreinament']+"','"+user['ableuseTechnology']+"');"
        print query
        cur.execute(query)
        user_id = str(cur.lastrowid)
        time = json['time'] 
        savetime(cur,time,'profile',user_id)
        commit(conn)
        return user_id
    except Exception, e:
        print e,'\nFail on trying to insert user to database.'
        return e
    finally:
            pass

   
    return user_id

@app.route("/profile",methods = ['PUT'])
def updateProfile():
    conn = connectDatabase()
    cur = conn.cursor()
    json = getResponse(request)
  
    try:
        user = json['data']
        user_nationality = t(user['nationality'])
        user = normalizeUser(user);
        user_id = json['id']
        time = json['time']
        query = "UPDATE users SET gender = '"+user['gender']+"',age = '"+str(user['age'])+"' ,occupation = '"+user['occupation']+"',education_degree = '"+user['highestLevel']+"',nationality = '"+user_nationality+"',language = '"+user['language']+"',agree_terms = '"+str(user['agree_terms'])+"',system = '"+user['system']+"',how_long_work = '"+user['howLong']+"',employment_status = '"+user['employmentStatus']+"',employment_status = '"+user['employmentStatus']+"',use_technology = '"+user['useTechnology']+"',computer_skills = '"+user['skills']+"',formal_training = '"+user['profileTreinament']+"',able_use = '"+user['ableuseTechnology']+"' WHERE id="+user_id+";"
       
        cur.execute(query)
        updateTime(cur,time,'profile',user_id)
        commit(conn)
        return user_id
    except Exception, e:
        print e,'\nFail on trying to update user to database.'
        return e
    finally:
        pass

@app.route("/questions", methods = ['POST'])
def savequestions():
    try:
        conn = connectDatabase()
        cur = conn.cursor()
        json = getResponse(request)
      
        answers = json['data']
        user_id = json['userId']
        step = json['step']
        index = 1
        for answer in answers:            
            query = "INSERT INTO answers (text,question_id,user_id,step) VALUES ('"+str(answer)+"','"+str(index)+"','"+user_id+"','"+step+"');"
            
            cur.execute(query)
            index += 1
        time = json['time'] 
        savetime(cur,time,"questions"+str(step),user_id)
        commit(conn)
        return str(cur.lastrowid)
    except Exception, e:
        raise e
        return e
    

@app.route("/questions", methods = ['PUT'])
def updatequestions():
    try:
        conn = connectDatabase()
        cur = conn.cursor()
        json = getResponse(request)
       
        answers = json['data']
        user_id = json['userId']
        step = json['step']
        index = 1
        for answer in answers:
            answer = t(answer)
            query = "UPDATE answers SET text = '"+str(answer)+"'  WHERE question_id = '"+str(index)+"'AND user_id= '"+str(user_id)+"' AND step = '"+step+"'"
            
            cur.execute(query)
            index += 1
        time = json['time'] 
        updateTime(cur,time,"questions"+str(step),user_id)
        commit(conn)
        return json['id']
    except Exception, e:
        raise e
        return e
    return null

@app.route("/step", methods = ['POST'])
def createstep():
    try:
        conn = connectDatabase()
        cur = conn.cursor()
        json = getResponse(request)
        
        ui = str(json['userId'])
        st = str(json['index'])
        sd = str(json['data'])
        query = "INSERT INTO steps_system (user_id,step,step_response) VALUES (%s,%s,%s);"
        
        cur.execute(query,(ui,st,sd))
        time = json['time'] 
        savetime(cur,time,str(st),ui)
        commit(conn)
        return str(cur.lastrowid)
    except Exception, e:
        raise e
        return e
@app.route("/step", methods = ['PUT'])
def updatestep():
    try:
        conn = connectDatabase()
        cur = conn.cursor()
        json = getResponse(request)
       
        ui = str(json['userId'])
        st = str(json['index'])
        sd = str(json['data'])
        query = "UPDATE steps_system SET step_response = %s WHERE user_id = %s AND step = %s"
        print query
        cur.execute(query,(sd,ui,st))
        time = json['time'] 
        updateTime(cur,time,str(st),ui)
        commit(conn)
        return str(json['id'])
    except Exception, e:
        raise e
        return e

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
        app.run(host='::',port=5034,debug=True)
