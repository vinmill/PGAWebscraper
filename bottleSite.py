from bottle import route, run, post, get, template, default_app
#Create bottle site
@route('/')
def menu():
    #return("Hi there")
    return template("main.html")

run(host='localhost', port=8080, debug=True)

