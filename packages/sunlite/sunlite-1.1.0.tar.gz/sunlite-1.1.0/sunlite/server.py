#all imports
from webbrowser import open_new
from datetime import datetime
from  os import  path,makedirs
from sunlite.db import connect
from  flask import  Flask , render_template , url_for , Markup
from flask_restful import  Resource,Api
import  logging
import json

import sunlite.server







db2 = '''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/png" href="https://github.com/sunx2/store_bin/raw/master/favicon.png">
     <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <title> Sunlite  Server : Root  </title>
</head>
<body>
<div class="w3-row w3-container w3-margin w3-padding w3-card-4">
    <div class="w3-half "><img  src="https://github.com/sunx2/store_bin/raw/master/logo.png" width="500px" height="500px"/>
    </div>

    <div class="w3-amber  w3-padding-48 w3-rest w3-sand w3-animate-opacity w3-margin">
        <h1 class="w3-text-blue-grey w3-center">Sunlite Server :  Root URL</h1> <br>

         <h2  class="w3-text-grey w3-center" > [  Link Panel - database :  {{DBname}}]</h2> <br>
        <div class="w3-margin w3-row">
            <a class="w3-half w3-button w3-indigo w3-card-4 w3-center w3-hover-white w3-hover-border-blue w3-hover-text-blue w3-text-white w3-padding-24" href="http://sunx2.github.io/sunlite">Sunlite Tutorials and Docs </a>
            <a class="w3-rest  w3-right w3-button w3-red w3-card-4 w3-center w3-hover-white w3-hover-border-red w3-hover-text-red w3-text-white w3-padding-24" href="https://github.com/sunx2/sunlite-demos">Github :  Sunlite Examples  </a>
        </div>
<h3 class="w3-center w3-margin-bottom w3-text-red w3-opacity" style="font-family: cursive">Making Easy More Easier !</h3>
    </div>
</div>
 <hr>

<div class="w3-row w3-container w3-margin w3-padding">
    <h3 class=" w3-text-grey w3-margin-bottom w3-bold w3-padding">  { Task Generator }</h3>
    <div class="w3-padding w3-half w3-border-left w3-border-amber">
        <select id="opt" class="w3-button w3-border-orange w3-border w3-text-orange w3-padding">
            <option class="w3-white w3-text-orange w3-hover-text-blue w3-hover-white w3-hover-white w3-hover-border-blue  w3-text-orange" value="new"  selected>Add Header </option>
            <option class="w3-white w3-text-orange w3-hover-text-blue w3-hover-white w3-hover-white w3-hover-border-blue  w3-text-orange" value="all">All headers</option>
            <option class="w3-white w3-text-orange w3-hover-text-blue w3-hover-white w3-hover-white w3-hover-border-blue  w3-text-orange" value="pull">Pull Data</option>
            <option class="w3-white w3-text-orange w3-hover-text-blue w3-hover-white w3-hover-white w3-hover-border-blue  w3-text-orange" value="get">Get Data</option>
            <option class="w3-white w3-text-orange w3-hover-text-blue w3-hover-white w3-hover-white w3-hover-border-blue  w3-text-orange" value="add">Add Data</option>
            <option class="w3-white w3-text-orange w3-hover-text-blue w3-hover-white w3-hover-white w3-hover-border-blue  w3-text-orange" value="db">All Data</option>
        </select>
        <div id="new" style="display: none" class="w3-margin w3-padding ">
            <input  id="hdoutput" class="w3-padding w3-input w3-boder w3-hover-border-blue w3-white w3-text-blue" placeholder="enter new header name" required/> <br>
            <button id="newbtn" class="w3-padding w3-border-orange w3-border w3-text-orange w3-white w3-hover-text-blue w3-card-2">Create</button>
        </div>
        <div id="all" style="display: none" class="w3-margin w3-padding ">
            <br><br>
            <button id="allbtn" class="w3-padding w3-border-pink w3-border w3-text-pink w3-white w3-hover-text-blue w3-card-2">Get headers</button>
        </div>
        <div id="pull" style="display: none" class="w3-margin w3-padding ">
            <input  id="pullit" class="w3-padding w3-input w3-boder w3-hover-border-red w3-white w3-text-red" placeholder="enter item name to pull" required/> <br>
            <button id="pullbtn" class="w3-padding w3-border-green w3-border w3-text-green w3-white w3-hover-text-blue w3-card-2">Pull</button>
        </div>
        <div id="get" style="display: none" class="w3-margin w3-padding ">
            <input  id="getit" class="w3-padding w3-input w3-boder w3-hover-border-red w3-white w3-text-red" placeholder="enter header name" required/> <br>
            <button id="getbtn" class="w3-padding w3-border-green w3-border w3-text-green w3-white w3-hover-text-blue w3-card-2">Get </button>
        </div>
        <div id="add" style="display: none" class="w3-margin w3-padding ">
            <input  id="add_name" class="w3-padding w3-input w3-boder w3-hover-border-green w3-white w3-text-green" placeholder="enter item name to push" required/> <br>
            <input  id="add_data" class="w3-padding w3-input w3-boder w3-hover-border-green w3-white w3-text-green" placeholder="enter item data to push" required/> <br>
            <input  id="add_header" class="w3-padding w3-input w3-boder w3-hover-border-green w3-white w3-text-green" placeholder="enter header name to push" required/> <br>
            <button id="addbtn" class="w3-padding w3-border-green w3-border w3-text-green w3-white w3-hover-text-blue w3-card-2">Push</button>
        </div>
        <div id="db" style="display: none" class="w3-margin w3-padding ">
            <br><br>
            <button id="dbbtn" class="w3-padding w3-border-pink w3-border w3-text-pink w3-white w3-hover-text-blue w3-card-2">Get all data</button>
        </div>

    </div>
    <div class="w3-rest w3-light-grey w3-text-gray w3-border w3-border-blue-grey w3-opacity">
        <h2 class="w3-center">Console</h2>
        <p class="w3-margin-left">    < started ...   </p> <br>
        <p class="w3-margin-left" id="console"></p>
    </div>

</div>

</body>
<!--<script src="{{url_for('static' , filename='ang.js')}}"></script>-->
<script>
     $('#opt').click(function() {
         var a = $(this).val()
         if (a=='new'){
             $("#new").show()
         }
         else {
             $("#new").hide()
         }
         if (a=='all'){
             $("#all").show()
         }
         else {
             $("#all").hide()
         }
          if (a=='pull'){
             $("#pull").show()
          }
         else {
             $("#pull").hide()
         }
         if (a=='get'){
             $("#get").show()
         }
         else {
             $("#get").hide()
         }
         if (a=='add'){
             $('#add').show()
         }
         else {
             $("#add").hide()
         }
         if (a=='db'){
             $("#db").show()
         }
         else {
             $("#db").hide()
         }
     })

    $("#newbtn").click(
        function() {
            var a = $("#hdoutput").val()
            $.get("/new/"+a, function(data, status) {
                $("#console").text("(" + status+")Data:  " + data.toSource())
            }   , 'json')})
    $('#allbtn').click(
        function() {
            $.get("/h", function(data, status) {
                $("#console").text("(" + status+") Data:  " + data.headers)
            }  ,'json')})
    $("#pullbtn").click(
        function() {
            var a = $("#pullit").val()
            $.get("/p/"+a, function(data, status) {
                $("#console").text("(" + status+")Data:  " + data.toSource())
            }   , 'json')})
    $("#getbtn").click(
        function() {
            var a = $("#getit").val()
            $.get("/g/"+a, function(data, status) {
                $("#console").text("(" + status+")Data:  " + data.toSource())
            }   , 'json')})
    $('#dbbtn').click(
        function() {
            $.get("/a", function(data, status) {
                $("#console").text("(" + status+")Data:  " + data.toSource())
            }  ,'json')})
    $("#addbtn").click(
        function() {
            var a = $("#add_name").val()
            var b = $("#add_data").val()
            var c = $("#add_header").val()
            $.get(  "/add/"+a+'/'+b+'/'+c  ,function(data, status) {
                $("#console").text("(" + status+")Data:  " + data.toSource())
            }   , 'json')})
</script>
</html>



'''


























class Serve(object):
       def __init__(self,name='',logs=True,logfolder=''):
              self.name = ":memory:" if name == '' else name
              if logs:
                     self.logs = True
                     logfolder = path.realpath(__file__) + "logs/{0}".format(str(datetime.today().date())) if logfolder=='' else logfolder
                     try:
                            makedirs(logfolder)
                     except:
                            pass
                     logtime = "time-{0}-{1}".format(datetime.now().time().hour,datetime.now().time().minute)
                     logfile = "{1}/database-{0}-{2}.log".format(self.name.replace(":",''),logfolder , logtime)
                     if path.exists(logfile):
                            logging.basicConfig(filename=logfile ,
                                         format='%(asctime)s %(message)s',
                                         filemode='a')
                     else:
                            logging.basicConfig(filename=logfile,
                                                format='%(asctime)s %(message)s',
                                                filemode='w')
                     self.logger = logging.getLogger()
                     self.logger.setLevel(logging.DEBUG)
                     self.logger.info("Sucess !  Logger Started. Writing logs on '{0}'".format(logfile))
              else:
                     self.logs = False
              with open("dump",'w') as f:
                     f.write(json.dumps({'name':self.name , 'logs':False}))
                     f.close()
              template_dir = path.realpath(sunlite.server.__file__).replace(path.basename(sunlite.server.__file__),'')
              template_dir = path.join(template_dir, 'templates')
              static_dir = path.join(template_dir,'static')
              self.APP = Flask(__name__ ,  template_folder=template_dir )
              self.API = Api(self.APP)
       def build_links(self):
              class MyDataManager(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                     def get(self, topic):
                            try:
                                   return {topic: str(self.co.pull(topic))}
                            except:
                                   return {topic: "doesn't exists"}
              class MyDataAddManager(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                            with open("Config",'r') as f:
                                   self.header = f.read()
                                   f.close()
                     def get(self, name , data,header=''):
                            header = self.header if header=='' else header
                            try:
                                   self.co.push(name,data,header)
                                   return {name: "Set Sucessfully"}
                            except:
                                   return {name: "Failed . Recheck data"}
              class MyFullData(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                     def get(self):
                            return  self.co.List()
              class MyAddHeader(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])

                     def get(self, name):
                            try:
                                   self.co.new(name)
                                   return {name: "Created New Header"}
                            except:
                                   return {name: "Failed . Recheck data"}
              class MyAllHeader(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])

                     def get(self):
                            try:
                                   return {'headers': self.co.headers()}
                            except:
                                   return {'headers' :"Failed . Recheck data"}
              class MyGet(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                     def get(self, name):
                                   try:
                                          return {name: self.co.get(name)}
                                   except:
                                          return {name: "Failed to fetch data"}
              self.API.add_resource(MyGet,'/g/<string:name>')
              self.API.add_resource(MyAllHeader,'/h/')
              self.API.add_resource(MyAddHeader,'/new/<string:name>')
              self.API.add_resource(MyFullData,'/a/')
              self.API.add_resource(MyDataAddManager,'/add/<string:name>/<string:data>/<string:header>')
              self.API.add_resource(MyDataManager, '/p/<string:topic>')

       def invoke(self,ip="127.0.0.1",port=5000):
              if self.logs:
                     self.logger.info("Sucess ! Api decleared.")
              if self.logs:
                     self.logger.info("Sucess ! Connected to {0}".format(self.name))
                     self.build_links()
              with open('dump', 'r') as f:
                     d = json.loads(f.read())
                     f.close()
              @self.APP.route('/')
              def HomePage():
                     #with open("main.html",'r') as f:
                       #     p = f.read()
                         #   f.close()
                     #return  render_template('main.html' , DBname=d['name'])
                     return db2.replace("{{DBname}}" , d['name'])
              if ip=='127.0.0.1' and port ==5000 :
                     open_new('http://localhost:5000/')
                     self.APP.run(debug=True)
              else:
                     try:
                            open_new('http://{0}:{1}/'.format(ip,port))
                            self.APP.run(host=ip,port=port  , debug=True)

                     except:
                            raise Exception('Invalied IP and Host : '+ip+':'+str(port))



