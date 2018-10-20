$( document ).ready(function() {
  
  //--------------------------------------------------- Style Buttons ---------------------------------------------------- 
  var backgroundImage = document.getElementById('img-style-background');
  
  
  //Add mars button listner
  var marsBtn = document.getElementById('mars-style-background');
  marsBtn.addEventListener('click', function(event) {
   backgroundImage.style = style="background-image:url('../assets/img/spaice/mars-background.jpg');";
  });
  
  //Add moon button listner
  var moonBtn = document.getElementById('moon-style-background');
  moonBtn.addEventListener('click', function(event) {
   backgroundImage.style = style="background-image:url('../assets/img/spaice/moon-background.jpg');";
  });
  
  
  //Add earth button listner
  var earthBtn = document.getElementById('earth-style-background');
  earthBtn.addEventListener('click', function(event) {
   backgroundImage.style = style="background-image:url('../assets/img/spaice/earth-background.jpg');";
  });
  
  
  //Add kandinsky button listner
  var kandinskyBtn = document.getElementById('kandinsky-style-background');
  kandinskyBtn.addEventListener('click', function(event) {
   backgroundImage.style = style="background-image:url('../assets/img/spaice/kandinsky-background.jpg');";
  });
  
  //Add vangogh button listner
  var vangoghBtn = document.getElementById('vangogh-style-background');
  vangoghBtn.addEventListener('click', function(event) {
   backgroundImage.style = style="background-image:url('../assets/img/spaice/vangogh-background.jpg');";
  });
  
  //Add davinci button listner
  var davinciBtn = document.getElementById('davinci-style-background');
  davinciBtn.addEventListener('click', function(event) {
   backgroundImage.style = style="background-image:url('../assets/img/spaice/davinci-background.jpg');";
  });
  //--------------------------------------------------- Drop zone ---------------------------------------------------- 
  
    

});

