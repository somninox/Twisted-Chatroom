from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
import time
import cgi

#this defines the webpage view to users

webcontent="""
<html>
	<head>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
	</head>
	<body>
		<h1>Send a message</h1>
		<form method="GET">Name: <input name="name" type="text" /><br />Message: <input name="chatline" type="text" /><input type="submit" value="Submit" /></form><br />

		<div id="CHAT">

		<table><tr><td>Name</td><td>Message</td></tr>%s</table>
		</div>
	</body>
	<script>
		function update_timer() {
			$.get("/CHAT",function(data) {
				$("#CHAT").load('/CHAT #CHAT');
				window.setTimeout(update_timer, 1000);
			});
		}
		window.setTimeout(update_timer,1000);
	</script>
</html>
"""

# adds and reads messages in the chatlog for users to view
class chatlog():
	def __init__(self):
		self.history=""

	def AddMessage(self,name,message):
		self.history+='<tr><td>%s</td> <td>%s</td></tr>' % (name, message)
		
	def readMessages(self):
		return self.history


# the user creates and sends a chat
class CHAT(Resource):	
	def render_GET(self, request):
		try:
			name=request.args["name"][0]
			message=request.args["chatline"][0]
			log.AddMessage(name,message)
			print("%s said %s" % (name, message))
		except:
			print("Probably AJAX")
		return webcontent % (log.readMessages()) 
			

class Redirect(Resource):  
	def render_GET(self, request):
		return '<META http-equiv="refresh" content="0;URL=/index.html">'

log = chatlog()

root = Resource()
root.putChild("", Redirect())
root.putChild("index.html", File("./"))
root.putChild("chatform.html", CHAT())
root.putChild("CHAT", CHAT())

mychatserver = Site(root)
reactor.listenTCP(9020, mychatserver)
reactor.run()