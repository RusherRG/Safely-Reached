var hamburger_on = false;
var hamburger = function()
{
    document.getElementById('sidepane').animate(
        [
            // keyframes
            { transform: 'translateX(-100%)' }, 
            { transform: 'translateX(0%)' }
          ], { 
            // timing options
            duration: 500,
            easing: 'ease-out'
          }
    ).onfinish = function(){
    document.getElementById('sidepane').style.transform = 'translateX(0)';
    }
    hamburger_on=true;

}

var hamburger_out = function()
{
    if(hamburger_on){
    document.getElementById('sidepane').animate(
        [
            // keyframes
            { transform: 'translateX(0%)' }, 
            { transform: 'translateX(-100%)' }
          ], { 
            // timing options
            duration: 500,
            easing: 'ease-out'
          }
        ).onfinish = function(){
        document.getElementById('sidepane').style.transform = 'translateX(-100%)';
        }
        hamburger_on=false;
        modal.style.display="none";
    }

}

window.addEventListener('load', async e => {
    
    console.log(navigator.onLine);
    if ('serviceWorker' in navigator) {
        try {
            navigator.serviceWorker.register('/serviceworker.js');
            console.log('SW registered');
        } catch (error) {
            console.log('SW failed');

        }
    }
   
    
    
});

var contacts = function()
{
    var userName = localStorage['userName'];
    var emc1 = localStorage['emc1'];
    var emc2 = localStorage['emc2'];
    var emc3 = localStorage['emc3'];
    var modal = document.getElementById('myModal');
    console.log(userName+' '+emc1);
    document.getElementById('userName').value = userName || '';
    document.getElementById('emc1').value = emc1 || '';
    document.getElementById('emc2').value = emc2 || '';
    document.getElementById('emc3').value = emc3 || '';

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal 
var modal = document.getElementById('myModal');
    
        modal.style.display="block";
    
}

var savecontact = function()
{
    console.log(document.getElementById('userName').innerText);
    localStorage['userName'] = document.getElementById('userName').value;
    localStorage['emc1'] = document.getElementById('emc1').value;
    localStorage['emc2'] = document.getElementById('emc2').value;
    localStorage['emc3'] = document.getElementById('emc3').value;
    var modal = document.getElementById('myModal');
    modal.style.display="none";
}

var closemodal = function()
{
    var modal = document.getElementById('myModal');
    modal.style.display = "none";
}


function getPsn(position) {
    var url = '/sos'
    var tosend = {
        username: localStorage['userName'] || '',
        emc1: localStorage['emc1'] || '',
        emc2: localStorage['emc2'] || '',
        emc3: localStorage['emc3'] || '',
        lat: position.coords.latitude,
        lng: position.coords.longitude
    }
    
    console.log(tosend);
    fetch(url, {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(tosend)
    }).then(response=>{console.log(response);
    alert('SOS Sent!')
    });
    
}

var sendsos = function(){
    navigator.geolocation.getCurrentPosition(getPsn);

}