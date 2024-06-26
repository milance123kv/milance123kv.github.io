from flask import Flask, request, render_template_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Srećan Rođendan Stevane</title>
  <meta charset="UTF-8" />
  <meta name="description" content="Srećan Rođendan Stevane">
  <link rel="icon" href="../../images/others/favicon.ico" type="image/x-icon" />
  <meta property="og:description" content="Wish you a very Happy Birthday">
  <link rel="stylesheet" type="text/css" href="../css/stylesheet.css">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta http-equiv="X-UA-Compatible" content="IE=9; IE=8; IE=7; IE=EDGE" />
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/balloon-css/0.5.0/balloon.min.css">
  <link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">
  <link href='https://fonts.googleapis.com/css?family=Signika' rel='stylesheet' type='text/css'>
  <link href='https://fonts.googleapis.com/css?family=Josefin+Sans:100,300' rel='stylesheet' type='text/css'>
  <script src="//cdnjs.cloudflare.com/ajax/libs/less.js/2.1.0/less.min.js"></script>
  <style>
    .inline-blocks > .block{
      display: inline-block;
      vertical-align: middle;
    }
    .image{
      height: 140px;
      width: 140px;
      border-radius: 180px;
      border: 3px solid #fff;
      margin-top: 22px;
      margin-right: 40px;
    }
    .twenty-one{
      font-size: 240px;
      font-family: 'Josefin Sans';
      font-weight: 100;
      line-height: 180px;
      color: #fff;
    }
    .bday{
      font-size: 24px;
      color: #fff;
      font-family: 'Josefin Sans';
      font-weight: 300;
      text-align: center;
    }
    .cover{
      background: rgba(0,0,0,0.82);
      width: 100%;
      height: 100%;
      top:0;
      left: 0;
      z-index: 1000;
    }
    #can{
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
    }
    div {
      overflow: auto;
    }
    .super-centered-container{
      display:flex;
      align-items: center;
      justify-content: center;
    }
    html,body{
      width: 100%;
      height: 100%;
      margin: 0;
      background:#131313;
    }
    a{
      color: skyblue;
      text-decoration: none;
    }
    .overlay-static{
      position: relative;
      z-index: 100;
      margin-bottom: 100px;
    }
    #myvideo{
      visibility: hidden;
    }
    body{
      background color: red ;
      /* background: url('../../images/humans/together/collage.jpg');*/
      background-position: center center;
      background-size: cover;
    }
    form {
      text-align: center;
      margin-top: 20px;
    }
    label, input, button {
      font-family: 'Josefin Sans', sans-serif;
      font-size: 18px;
      margin: 5px;
    }
    button {
      padding: 5px 10px;
    }
  </style>
</head>
<body>
  <div>
    <audio id="hbd" class="song" controls autoplay loop>
      <source src="../../audio/hbd1.mp3" type="audio/mpeg"></source>
      Your browser isn't invited for super fun audio time.
    </audio>
  </div>
  <div class="cover super-centered-container">
    <canvas id="can">Get a browser</canvas>  
    <div class="overlay-static">    
      <div class="inline-blocks">
        <h2 class="twenty-one block">2</h2>
        <img class="image block" src="../../images/humans/together/us1.jpg">
        <h2 class="twenty-one block"> 2</h2>
        <img class="image block" src="../../images/humans/together/us2.jpg">
      </div>
      <h1 class="bday">Srećan Rođendan <a target="_self" rel="noopener noreferrer" href="../../index.html"> Stevo</a></h1>
      <form action="/send_email" method="post">
        <label for="email">Unesite vaš email:</label>
        <input type="email" id="email" name="email" required>
        <button type="submit">Pošalji</button>
      </form>
    </div>
  </div>
  <script>
    const TwoPI = Math.PI * 2;
    var w = window.innerWidth;
    var h = window.innerHeight;
    var center_x = w / 2;
    var center_y = h / 2;
    var colors = ['#FF0000', '#E8D45B', '#8CFF00','#3F33FF','#FF3349','#33FFC7']
    var max_distance = Math.abs(Math.max(center_x, center_y));
    var min_distance = Math.abs(Math.min(center_x, center_y));

    function Firefly(){
      this.velocity = 0;
      var random_angle = Math.random() * TwoPI;
      this.x = center_x +  Math.sin(random_angle) * ((Math.random() * (max_distance - min_distance) + min_distance));
      this.y = center_y + Math.cos(random_angle) * ((Math.random() * (max_distance - min_distance) + min_distance));
      this.angle_of_attack = Math.atan2(  this.y - center_y ,  this.x - center_x);
      this.vel =  ( Math.random() * 50 ) + 20 ;
      this.color = colors[ ~~(colors.length * Math.random()) ]
      this.xvel = this.vel * Math.cos( this.angle_of_attack );
      this.yvel = this.vel * Math.sin( this.angle_of_attack );
      this.size = 2 + Math.random() * 2;
      this.phase_diff = Math.random() * TwoPI;
    }

    Firefly.prototype.move = function(dt){
      if( isOnHeart(this.x, this.y)){
        this.size -= 0.001;
        return;
      }
      this.x += this.xvel * dt;
      this.y += this.yvel * dt;
    }

    Firefly.prototype.render = function(ctx, now){
      if( this.size < 1) {
        return;
      }
      ctx.globalAlpha = Math.max(Math.abs(Math.sin( (now + this.phase_diff) / (~~(this.size * 100)) )), 0.4);
      ctx.fillStyle = this.color;
      ctx.shadowColor = this.color;
      ctx.shadowBlur = 20 / this.size; 
      ctx.beginPath();
      ctx.arc( this.x, this.y, this.size, 0, TwoPI, false);
      ctx.closePath();
      ctx.fill();
    }

    var max_fireflies = 500;
    var canvas = document.getElementById('can');
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var fireflies = [];
    var last = Date.now();
    var dt = 0, now = 0;
    var alive_fireflies = 0;
    var last_emit = 0;

    function render(){
      var audio = document.getElementById("hbd");
      audio.play();
      now = Date.now();
      dt = (last - now) / 1000; 
      last = now;
      ctx.clearRect(0,0,w,h);
      fireflies.forEach(function(f){
        f.move(dt);
        f.render(ctx, now);    
      });
      fireflies = fireflies.filter(function(f){
        return (f.size > 1);
      });
      alive_fireflies = fireflies.length;  
      if( alive_fireflies < max_fireflies && last_emit - now < - 100){
        fireflies.push( new Firefly());
        last_emit = now;
      }
      requestAnimationFrame(render);
    }

    render();

    function isOnHeart(x,y){
      x = ((x - center_x) / (min_distance * 1.2)) * 1.8;
      y = ((y - center_y) / (min_distance)) * - 1.8;
      var x2 = x * x;
      var y2 = y * y;
      return (Math.pow((x2 + y2 - 1), 3) - (x2 * (y2 * y)) <= 0);
    }

    function HideOrShow(cur_div){ 
      var current=document.getElementById(cur_div);
      if(current.style.visibility=="hidden") {
        current.style.visibility ="visible";
      } else {
        current.style.visibility ="hidden";
      }
    }
  </script>
</body>
</html>
"""
from flask import send_file


def send_email(receiver_email):
    sender_email = "milance99kv@gmail.com"
    sender_password = "kwxq gdsv blfd vfyo"
    subject = "Srećan Rođendan Mogli!"
    body = "Izvoli svoj poklon. Srećan rođendan još jednom!"
    filename = "projekat\src\html\poklon.mp4"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
@app.route('/surprise')
def surprise():
    return send_file('projekat/src/html/surprise.html')

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/send_email', methods=['POST'])
def email():
    email = request.form['email']
    send_email(email)
    return "Poslat je mejl!"

if __name__ == '__main__':
    app.run(debug=True)
