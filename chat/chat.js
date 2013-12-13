// Load the TCP Library
net = require('net');
 
// Keep track of the chat clients
var bars = {};
 
// Start a TCP Server
net.createServer(function (socket) {
 
	// Identify this client
	socket.ip = socket.remoteAddress; 

	// Handle incoming messages from clients.
	socket.on('data', function (data) {

		// parse the json data
		data = JSON.parse(data);
		console.log(data);

		// get the command and do something
		switch (data.command) {
			case "join": {
				
				// add user data to the socket
				socket.uid  = data.uid;
				socket.name = data.name;
				socket.bar  = data.bar;
				socket.sex  = data.sex;
				
				// create chat for bar if it doesn't exist
				// then add the user
				if (!(socket.bar in bars)) {
					bars[socket.bar] = [socket];
				}

				// success
				socket.write(JSON.stringify({success: true}));
				break;
			}
			case "leave": {
				
				// remove the person from the bar
				bars[socket.bar].splice(bars[socket.bar].indexOf(socket), 1);
				
				// success
				socket.write(JSON.stringify({success: true}));
				break;
			}
			case "chat": {
				sendToBar(bars[socket.bar], data.message);
			}
		}
	});

	// Remove the drinker from the list when it leaves
	socket.on('end', function () {
		bars[socket.bar].splice(bars[socket.bar].indexOf(socket), 1);
		sendToBar(bars[socket.bar], socket.name + " has left the chat!");
	});

	// Send a message to all people in this bar
	function sendToBar(bar, message) {
		bar.forEach(function (client) {
			var toSend = JSON.stringify({uid: sender.uid, name: sender.name, message: message});
			console.log(toSend);
			client.write(toSend);
		});
	}
 
}).listen(9992);
 
// Put a friendly message on the terminal of the server.
console.log("Chat server running at port 9992\n");
