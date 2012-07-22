/* PROSÍM NEPOUŽÍVEJTE PØÍMÉ LINKY, BEZ ÈASOVÉHO ODPOÈTU NEBUDOU FUNKÈNÍ */

function CountDown(t){
 if (t-->1){
   setTimeout("CountDown("+t+")",1000);
   document.getElementById('count_down').innerHTML=t;
 }
 else{
  document.getElementById('count_down').style.display='none';
  document.getElementById('downdiv').style.display='block';
  ClearInfo('');
 }
}

function FinishDown(){
  var link=document.getElementById('downlink');
  document.location=link.getAttribute('href');
}

function ClearInfo(s){
  try{
   parent.document.getElementById('downinfo').innerHTML=s;
  }
  catch(err){
  }
}
