(function () {
   
    // strict syntax
    'use strict';

    // import the socket.io lib and bind to port 9000
    var io = require('socket.io').listen(9000);

    // broadcast to a bar
    function broadcastToBar (socket, bar, data) {
        for (var i=0; i<bar.length; i++) {
            bar[i].emit('chat', data);
        }
    }

    // everytime someone connects
    io.sockets.on('connection', function (socket) {
        
        // the bars
        var bars = {};

        // request login
        socket.emit('login', { request: true });

        // first, check for the login
        socket.on('login', function (data) {
       
            // set data to the socket
            socket.userId = data.userId;
            socket.barId  = data.barId;
            socket.name   = data.name;

            // check to see if the bar exists first
            if (data.barId in bars) {
                bars[data.barId].push(socket);
            } else {
                bars[data.barId] = [socket];
            }
        
        });

        // check for leaving the bar as well
        socket.on('leave', function (data) {
            bars[socket.barId].splice(bars[socket.barId].indexOf(socket), 1);
            broadcastToBar(socket, bars[socket.barId], { userId: socket.userId, name: socket.name, leave: true });
        });

        // check for any messages
        socket.on('chat', function (data) {
            broadcastToBar(socket, bars[socket.barId], { userId: socket.userId, name: socket.name, message: data.message }); 
        });

        // get a list of people in the bar
        socket.on('list', function (data) {
                
            // build list from sockets
            var bar = bars[socket.barId];
            var drinkers = [];
            for (var i=0; i<bar.length; i++) {
                drinkers.push({ name: bar[i].name, userId: bar[i].userId });
            }
            socket.emit('list', { "drinkers": drinkers });
        });

    });

}());
