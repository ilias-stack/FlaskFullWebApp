//showing & hiding the table


const show=document.getElementById("table");
const ArtsAll=document.getElementById("artclInfo");
show.addEventListener('click',()=>{
    if (show.innerText=='Show table'){
    ArtsAll.style.display='block'
    show.innerText='Hide table'

    }
    else if (show.innerText=='Hide table'){
        ArtsAll.style.display='none';
        show.innerText='Show table'
    }
});

//filtring the table

const search=document.getElementById('search');
const bar=document.getElementById('TOsearch');
const recup=ArtsAll.innerHTML
search.addEventListener('click',()=>{
    ArtsAll.innerHTML=recup;
    let num=document.getElementsByTagName('tr');
    for (j=0;j<num.length+100;j++){
    for (i=1;i<num.length;i++){
        if(!num[i].innerHTML.includes(bar.value)){
            num[i].remove()
        }
       
    }
    }
    ArtsAll.style.display='block'
    show.innerText='Hide table'
});





//artcl_changer verifier
let inps=document.getElementsByTagName('input');
setInterval(()=>{
    if(inps[1].value!='' && inps[2].value!='' && inps[3].value!='' && inps[4].value!='' &&inps[5].value!='' && inps[6].value!='' && inps[7].value!=''){
        document.getElementById('change').style.display='inline'
    }
    else{
        document.getElementById('change').style.display='none'
        
    }
},200)




//zone info articles





window.addEventListener('keydown', function(e) {
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        e.preventDefault();
        return false;
    }
}, true);





// Trier les fournisseures

try{const fourns=document.getElementById("fournisseure");
let tout=document.getElementById('scrollArts');
let backup=tout.innerHTML;
let elmnts=document.getElementsByClassName('IMG');
let fourn;

fourns.addEventListener('change',()=>{
    tout.innerHTML=backup;
    let choosenFourn=[];
    for(i=0;i<elmnts.length;i++){
        fourn=elmnts[i].outerHTML;
        if(fourn.includes(fourns.value)){
            choosenFourn+=(fourn)
        }
    }
    tout.innerHTML=choosenFourn;

    if(fourns.value=='All'){
        tout.innerHTML=backup;
    }

});

document.getElementById('refresh').addEventListener('click',()=>{
    window.location.reload()
})



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
});}

catch{

}



//auto fill for the Admin

let tablo=document.getElementsByTagName('tbody')[0];
let divisions=tablo.innerHTML.toString().split('<tr>').slice(1);
let data,allData=[];
inps[1].addEventListener('input',function(e){
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        console.log('OK')
    }
    for (let i=0;i<divisions.length;i++){
        data=divisions[i].split('\n');
        for(j=0;j<data.length;j++){
            data[j]=data[j].replace('<td>','').replace('</td>','').trim();
        }
        data=data.slice(1,data.length-4)
        allData.push(data) 
    }
    for(i=0;i<allData.length;i++){
    if(inps[1].value==allData[i][0]){
        inps[2].value=allData[i][1]
        inps[3].value=allData[i][2]
        inps[4].value=allData[i][3]
        inps[5].value=allData[i][4]
        inps[6].value=allData[i][5]
        inps[7].value=allData[i][6]
        break;
    }
    else if (inps[1].value!=allData[i][0]){
        inps[2].value=''
        inps[3].value=''
        inps[4].value=''
        inps[5].value=''
        inps[6].value=''
        inps[7].value=''
    }
      }
      
})

//auto fill for nonAdmin
document.getElementById('choices').addEventListener('change',()=>{
    inps[1].value=(document.getElementById('choices').value);
    for (let i=0;i<divisions.length;i++){
        data=divisions[i].split('\n');
        for(j=0;j<data.length;j++){
            data[j]=data[j].replace('<td>','').replace('</td>','').trim();
        }
        data=data.slice(1,data.length-4)
        allData.push(data) 
    }
    for(i=0;i<allData.length;i++){
    if(inps[1].value==allData[i][0]){
        inps[2].value=allData[i][1]
        inps[3].value=allData[i][2]
        inps[4].value=allData[i][3]
        inps[5].value=allData[i][4]
        inps[6].value=allData[i][5]
        inps[7].value=allData[i][6]
        break;
    }
    else if (inps[1].value!=allData[i][0]){
        inps[2].value=''
        inps[3].value=''
        inps[4].value=''
        inps[5].value=''
        inps[6].value=''
        inps[7].value=''
    }
      }
})
