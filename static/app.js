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
    }

}