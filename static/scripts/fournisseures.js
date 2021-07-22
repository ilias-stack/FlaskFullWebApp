
const formulaire=document.getElementById('formulaire');
const f=document.getElementById('Form');


const sign=document.getElementById('reg')
let inps=document.getElementsByTagName('input');
setInterval(function(){
    if (inps[0].value!='' && inps[1].value!='' && inps[2].value!='' && inps[3].value!='' && inps[4].value!='' && inps[5].value!='' && inps[6].value!='' && inps[4].value==inps[5].value && inps[3].value.startsWith('+212') ){
        sign.style.display='inline'
    }   
    else{
        sign.style.display='none'
    }     
    
    
},10)

function noenter() {
    return !(window.event && window.event.keyCode == 13); }



window.addEventListener('keydown', function(e) {
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        e.preventDefault();
        return false;
    }
}, true);


function ranMDP(){
    let L=[];
    for(let i=0;i<6;i++){
        L+=[Math.floor(Math.random()*10)]
    }
    return L.toString()
}

const passwd=document.getElementById('MDP');
passwd.onkeyup = function(e){
    if(e.keyCode == 17){
        let passi=ranMDP();
        inps[5].value=passi;
        inps[4].value=passi;
    }
}



document.getElementById('logo').addEventListener('click',()=>{
    window.location.href = "/"
})


document.getElementById('MGSii').addEventListener('click',()=>{
  if(document.getElementById('drop').style.display=='none'){
    document.getElementById('drop').style.display='block'
  }
  else{
    document.getElementById('drop').style.display='none'
  }
})