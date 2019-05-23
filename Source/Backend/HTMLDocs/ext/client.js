class client {
    Socket;
    container;

    constructor(UID){
        super();
        this.Socket = new WebSocket('ws://' + window.location.host + '/ws/Socket/' + UID)
        this.Socket.onmessage = function(e){
            var data = JSON.parse(e.data);
            var message = data['message'];
            this.container = message;
        };

        this.Socket.onclose = function(e){
            console.error('Socket closed unexpectedly. Connetion lost?');
        };

        console.log('Client : connected.')
    }

    __sent(data){
        this.Socket.send(JSON.stringify({
            'content': data,
            'type' : 'OFFER',
        }));
    }

    __request(data){
        this.Socket.send(JSON.stringify({
            'content': data,
            'type' : 'REQUEST',
        }));
    }
}
