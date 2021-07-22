// Sticky top property SET

window.addEventListener('scroll',function(){
    const nav_B=document.getElementById('navig')
    let y_CORD=(window.scrollY);
    if (y_CORD>63){
      nav_B.classList.add("sticky");
    }
    else{
      nav_B.classList.remove("sticky");
    }
  });


//Search bar setup

let btnS=document.getElementById('find');
const Art_list=document.getElementsByClassName('article')
let S_bar=document.getElementById('bar');
let all_ARTS=document.getElementById('all');
let Art;
let backup=all_ARTS.innerHTML;


btnS.addEventListener('click',()=>{
  let choosenArt=[];
  all_ARTS.innerHTML=backup;

  for (i=0;i<Art_list.length;i++){
    Art=Art_list[i].outerHTML;

    if(Art.includes(S_bar.value)){
      choosenArt+=(Art_list[i].outerHTML)
    }
  }
  all_ARTS.innerHTML =choosenArt
});
