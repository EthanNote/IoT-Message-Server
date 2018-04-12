// Empty JS for your own code to be here

var lastRecv=null
var list=null

$(document).ready(function() {

            namespace = '/log';

            var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);


            socket.on('event', function(msg) {
                //console.log(msg);
                //console.log("DEBUG 1");
                //document.getElementById("msg-list").append("DEBUG");
                //$(".msg-list")[0].append("message<br />");
                lastRecv=msg;
                //var line=$("<div></div>").text(JSON.stringify(msg))

                var line=document.createElement("div");
                line.innerText=JSON.stringify(msg);
                list= $(".msg-list")[0];
                list.append(line);
                line.scrollIntoView()
                while(list.childElementCount>300){
                    list.firstChild.remove()
                }
            });

        });