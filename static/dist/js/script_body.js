function printfunction(){
    console.log('submitted');
  }

  var containerlist = document.getElementsByClassName('single__email');
  document.addEventListener('click', function (event) {
    var flag;
    flag = 0;
    for (i = 0; i < containerlist.length; i++) {
      container = containerlist[i];
      if (container !== event.target && !container.contains(event.target)) {
        flag = flag || 0;
      }
      else {
        flag = 1;
        
        j = i;
        i = containerlist.length - i - 1;
        x = i.toString();
        id_name = 'singleemail_'+x;
        var s_name = document.getElementById(id_name).getElementsByClassName('__name')[0].innerHTML;
        var s_date = document.getElementById(id_name).getElementsByClassName('__date')[0].innerHTML;
        var s_sub =  document.getElementById(id_name).getElementsByClassName('__subject')[0].innerHTML;
        var s_msg = document.getElementById(id_name).getElementsByClassName('__message')[0].innerHTML;
        s_msg = escape_html(s_msg)
        var sender =  document.getElementById(id_name).getElementsByClassName('__sender')[0].innerHTML; //document.getElementById('msg1').innerHTML;
        console.log(sender);
        console.log(s_name);
        console.log("------")
      
        document.getElementById('sname').innerHTML = s_name;
        document.getElementById('mname').innerHTML = sender;
        //"anishshende001@gmail.com";
        var check = sender;    
        console.log("CHECK VALUE: ",check);    
        document.getElementById('rname').innerHTML = "anish@gmail.com";
        document.getElementById('sendersubject').innerHTML = s_sub;
        document.getElementById('sendermessage').innerText = s_msg;

        //reply box config
        if(check == null)
        {
          console.log("value not printed");
        }
        var x = document.getElementById('rep_recvname').value;
        console.log("value of: ",x);
        document.getElementById('rep_send_subject').value = "Re:"+s_sub;
        document.getElementById('rep_id').value=i+1;
        break;
      }
    }
    if (flag == 1) {
      console.log('clicking inside the div');
    }
    else {
      console.log('clicking outside the div');
    }
  });

function click_handler() {
    var x = document.getElementById('__composebox');
    if(x.style.display=="none"){
      x.style.display = "block";
    }
    else {
      x.style.display = "none";
    }
  };

function compclosefunction() {
    var x = document.getElementById('__composebox');
    if(x.style.display=="none"){
      x.style.display = "block";
    }
    else {
      x.style.display = "none";
    }
  };

function repclosefunction() {
    var x = document.getElementById('__replybox');
    if(x.style.display=="none"){
      x.style.display = "block";
    }
    else {
      x.style.display = "none";
    }
  };


function replyFunction() {
    var x = document.getElementById('__replybox');
    
    // document.getElementById("replytextheader").innerHTML = "Reply Message";
    to_send = document.getElementById("mname").innerHTML;
    document.getElementById("rep_recvname").value=to_send;
    if(x.style.display=="none"){
      x.style.display = "block";
    }
    else {
      x.style.display = "none";
    }
  }

function fwdFunction() {
    var x = document.getElementById('__replybox');
    if(x.style.display=="none"){
      x.style.display = "block";
    }
    else {
      x.style.display = "none";
    }
    document.getElementById("replytextheader").innerHTML = "Forward Message";
  }

function escape_html(str){
    return str.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
 }