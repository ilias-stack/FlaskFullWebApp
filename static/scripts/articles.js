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





//artcl_creator verifier
const ADD=document.getElementById('ajout');
const RAM=document.getElementById('RAM')
const GPU=document.getElementById('GPU')
const Prix=document.getElementById('Prix')
const REF=document.getElementById('REF');

setInterval(()=>{
    let valable=['OUI','NON'];
    let a=GPU.value
    let b=RAM.value;
    if(b.includes('GB') && valable.includes(a) && document.getElementById('NOM').value!='' && document.getElementById('stockage').value!='' && document.getElementById('Prix').value!='' && REF.value!=''){
        ADD.style.display='inline';
    }
    else{
        ADD.style.display='none';
    }
},100)


//zone info articles
let tablo=document.getElementsByTagName('table')[0].rows;



setInterval(()=>{
    let tva=document.getElementById('TVA');
    let ref=document.getElementById('REFer');
    let ht=document.getElementById('HT');
    let ttc=document.getElementById('TTC');
    let cond_table=[];
    tva=parseInt(tva.value)/100
    tva=eval(1+tva)
    let samp,samp2;
    let val;
    if (ref.value=='' ){
        ht.value='';
        ttc.value='';
    }


    else{
    for(i=1;i<tablo.length;i++){
    samp=tablo[i].innerHTML;
    samp2=tablo[i].innerHTML.toString().trim().split('\n')
    samp2=samp2[0].replace('<td>','').replace('</td>','')
    cond_table.push(samp2==(ref.value))
    if(cond_table.includes(true)){
        val=tablo[cond_table.indexOf(true)+1].innerHTML.toString().trim().split('\n')
        val=parseInt(val[val.length-1].replace('<td>','').replace('</td>',''));
        ht.value=val;
        ttc.value=Math.floor(eval(val*tva));
    }
    else{
        
        ht.value='NOT FOUND';
        ttc.value='NOT FOUND';

    }
    


    }
}

},100)


window.addEventListener('keydown', function(e) {
    if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
        e.preventDefault();
        return false;
    }
}, true);





// Trier les fournisseures

const fourns=document.getElementById("fournisseure");
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
})