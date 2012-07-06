// Copyright Martevax 2004-2012 
//  souË·st aplikacÌ pro www.titulky.com



 function Compatability(){ 
 }
 
 
 function CheckUpload(p){
     for (a=4;a>=1;a--){
         v=eval('document.Upload_form.Soubor'+a+'.value');
         if (v>''){
           for (b=a;b>=1;b--){
              v2=eval('document.Upload_form.Soubor'+b+'.value');
              if (v2==''){
                 alert('Titulky musÌte vkl·dat postupnÏ. Nem˘ûete nahr·vat titulky k CD'+a+' a p¯eskoËit CD'+b);
                 return false;
              }


              v3=eval('document.Upload_form.VelikostFilmu'+b+'.value');
              if (v3==""){
                 if (!confirm("Chcete pokraËovat d·le, p¯estoûe nenÌ vyplnÏna velikost filmu pro CD"+b+"?")){
                   eval('document.Upload_form.VelikostFilmu'+b+'.focus()');                     
                   return false;
                 }                 
              }
              else if(isNaN(v3) || parseInt(v3)<10000){
                  alert("Chybn· hodnota, velikost filmu uveÔte prosÌm v bytech");
                  eval('document.Upload_form.VelikostFilmu'+b+'.select()'); 
                  return false;
              }
        
        
                      
           }
         }
         if (v=='' && a==1){
            alert ('Vyberte soubor s titulky');
            return false;
         }
     }
     if (document.Upload_form.SQLsNazev.value==''){
         alert ('Zadejte n·zev titulk˘');
         return false;
    }
    if(document.Upload_form.SQLnRokUvedeni.value>''){
        var datum = new Date();
        ROK=datum.getFullYear();
        if(document.Upload_form.SQLnRokUvedeni.value<1901 || document.Upload_form.SQLnRokUvedeni.value>ROK){
              alert("Rozsah roku m˘ûe b˝t 1901 - "+ROK);
              return false;
        }
    }    

 if (p<1){return confirm('P¯ejete si opravdu provÈst upload, p¯estoûe nejste p¯ihl·öeni?')}
 return true;
 }
 
 
 function TestAll(formset){
         var strPrefix="";
        if (formset.SQLsPuvodniNazev.value==""){
          if (!confirm("Chcete pokraËovat d·le, p¯estoûe nenÌ vyplnÏn alternativnÌ (p¯eloûen˝) n·zev filmu?\nPokud ofici·lnÌ p¯eklad nezn·te (nebo V·s nenapad· nic, ËÌm by se zjednoduöilo vyhled·v·nÌ) tak jej nevyplÚujte!"+strPrefix)){
          formset.SQLsPuvodniNazev.focus();           
           return false;
           }
        }
        if (formset.SQLsReleas.value==""){
          if (!confirm("NenÌ vyplnÏn release DivX filmu. Bez tÈto informace velmi znesnadnÌte orientaci z·jemc˘ o tyto titulky. Chcete p¯esto pokraËovat?"+strPrefix)){
             formset.SQLsReleas.focus();                     
             return false;
           }
        }

        if (formset.SQLncTyp.value==0){
                 if (!confirm("Jste si jisti vyplnÏnÌ typu titulk˘ na NEZN¡M› typ ?"+strPrefix)) {
                    formset.SQLncTyp.focus();
                    return false;
                 }
        }
        if (formset.SQLsJazyk.value==''){
                 alert('Zvolte prosÌm jazyk titulk˘');
                 formset.SQLsJazyk.focus();
                 return false;
        }
        /*
        if (formset.SQLsNote.value.length>255){
                 alert('Pozn·mka m˘ûe obsahovat pouze 255 znak˘, prosÌm zkraùte text o '+(formset.SQLsNote.value.length-255)+' znak˘');
                 formset.SQLsNote.focus();
                 return false;
        }
        */                
        if (formset.SQLsIMDB.value=="" || formset.SQLsIMDB.value=='0000000'){
             alert("NenÌ vyplnÏno ID dle mezin·rodnÌ filmovÈ datab·ze IMDb, bez nÏhoû nelze titulky uloûit a n·slednÏ st·hnout. Toto ËÌslo zjÌstÌte na www.imdb.com po zad·nÌ n·zvu filmu do vyhled·vacÌho pole a zvolenÌm p¯ÌsluönÈho detailu filmu z URL."+strPrefix);
             formset.SQLsIMDB.focus();
             return false;
        }
        else{
             if (window.RegExp)
             {
              re = new RegExp("^[0-9]{3,8}$");
              if (!re.test(formset.SQLsIMDB.value))
              {
              alert("Chyba v IMDB, musÌ obsahovat pouze poslednÌch 8 ËÌsel z URL");
              //formset.SQLsIMDB.value='';
              formset.SQLsIMDB.select();
              return false;
              }
        }
      }  
}
 
function CheckIMDB(formset){
        if (formset.SQLsIMDB.value==""){
           alert('NenÌ vyplnÏno ID dle mezin·rodnÌ filmovÈ datab·ze IMDb, bez tÈto identifikace nebude moûnÈ poûadavek zapsat');
           formset.SQLsIMDB.focus();
           return false;
        }
        else{
             if (window.RegExp)
             {
              re = new RegExp("^[0-9]{3,8}$");
              if (!re.test(formset.SQLsIMDB.value))
              {
              alert("Chyba v IMDB, musÌ obsahovat pouze poslednÌch 8 ËÌsel z URL");
              formset.SQLsIMDB.select();
              return false;
              }
        }
      } 
      return true;
} 


function LoadPoz(){
   document.pozadavek.odesl_poz.disabled=true;
   var v=document.getElementById('imdb').value.toString();
   document.getElementById('iframehid').src='iframe_poz.php?IMDB='+ escape(v);
}

 
function positionedOffset(element) {
    var valueT = 0, valueL = 0;
    do {
      valueT += element.offsetTop  || 0;
      valueL += element.offsetLeft || 0;
      element = element.offsetParent;
    } while (element);

    return {x:valueL, y:valueT};
}

function SR(e,o,show){
 return;
 var o2=o.parentNode;
 var title=o2.getAttribute('title');
 var b=document.getElementById("release");
 if (show){

     var pos = positionedOffset(o);

     b.style.top= (pos.y-5)+'px';
     b.style.left= (pos.x+14)+'px';
     b.innerHTML=title;    
    o2.title="";
    b.style.display='block';
 }
 else{
    o2.title=b.innerHTML;
    b.style.display='none';
 }
} 
 
 
  function PartString(vstup,cast){
	   var intC,intB,intD=0;
		 var vystup='';
		 var intB=vstup.indexOf(cast);
		 if (intB==-1) return false;
		 for (intC=intB;intC<vstup.length && vstup.charAt(intC)!=';';intC++){
				 if (cast.length<=intD++){
				  vystup+=vstup.charAt(intC);
				 } 
		 } 
  return vystup;
	}



function xy_offset() {
  w=document.body.offsetWidth;
  h=document.body.offsetHeight;
  document.body.scrollLeft+(w-300)/2;
  document.body.scrollTop+(h-85)/2;
  alert (w+' '+h);
}


function CheckDiskuze(f){
 if (f.SQLsText.value==''){
     return false;
 }
 else {
     if (!f.Souhlas.checked){
       alert('Je nutnÈ souhlasit s podmÌnkami pro zaps·nÌ koment·¯e');
       return false;
     }
     return true;
 }
}

function Reply(cislo){
  with(document.formDiskuze){
    //SQLsNadpis.value="RE: "+n;
    //SQLsNadpis.style.backgroundColor='#efefef';
    //SQLsNadpis.readOnly=true;
    SQLnParent.value=cislo;
  }
}
function NoReply(){
  if (document.formDiskuze.SQLsNadpis!=null){
    document.formDiskuze.SQLsNadpis.readOnly=false;
    document.formDiskuze.SQLsNadpis.style.backgroundColor='#ffffff';
  }
  document.formDiskuze.SQLnParent.value='';
}

function Reply2(cislo){
  var o=document.getElementById('pr_'+cislo);
  //var t=o.firstChild.nodeValue;
  var t='';
	var a=o.getAttribute('headers');
  with(document.formDiskuze){
    SQLsNadpis.value="RE: "+t;   
    SQLsNadpis.style.backgroundColor='#efefef';
    SQLsNadpis.readOnly=true;
    SQLnParent.value=cislo;
    SQLnVnoreni.value=a;
    SQLsText.focus();
  } 
}


function Nahled(w,tit,histstamp){  
  var o=document.getElementById('div_nahled');
  if (w<1){
    o.style.visibility='hidden';
    o.style.height='1px';
  }
  else{
    if(w==2){
      document.getElementById('IframeNahled').src="downahled.php";
    }else{
      document.getElementById('IframeNahled').src="nahled.php?Titulky="+tit+"&histstamp="+histstamp;
    }  
    o.style.height='700px';
    o.style.visibility='visible';
  }
}
function Trvale(o){
if (o.checked){
 if(!confirm('Chcete b˝t prihl·öeni trvale?'))o.checked=false;
 }
}


function OpenDownload(d,zip,h){
   var Stamp = new Date();
   var err=false;
   if (!err){
     document.getElementById('downinfo').innerHTML='Poûadavek na staûenÌ se za¯azuje, prosÌm Ëekejte';
     var o=document.getElementById('idown');
     o.style.display='block';
     o.style.height='500px';
     o.style.width='612px';
     o.style.border='none';
     var odkaz='idown.php?R='+Stamp.getTime()+'&titulky='+d+'&zip='+zip+'&histstamp='+h
     document.documentElement.scrollTop=0;//245;
     o.src=odkaz;
     //document.frames['idown'].location=odkaz;
   }
   else{
     alert("Nekompatibilita prohlÌûeËe nebo nÏkterÈho pluginu nap¯. Adblock, kter˝ blokuje zobrazov·nÌ obsahu str·nek");
     //return false;
   }
}

function OpenDownloadX(d,zip,h){
   var Stamp = new Date();
   var rnd='okno'+Stamp.getTime();
   var el=document.getElementById("IframeDownload");
   frames['IframeDownload'].location.href='/download.php?R='+rnd+'&Titulky='+d+'&zip='+zip+'&histstamp='+h;
   window.open('http://primadvd.cz',rnd);
   //window.open('download.php?R='+Stamp.getTime()+'&Titulky='+d+'&zip='+zip+'&histstamp='+h,'IframeDownload');  
   //el.src='download.php?R='+Stamp.getTime()+'&Titulky='+d+'&zip='+zip+'&h='+h;
}


function AjaxDownload(d,zip){
   var Stamp = new Date();
   var el=document.getElementById("IframeDownload");
   var strURL ='download.php?R='+Stamp.getTime()+'&Titulky='+d+'&zip='+zip;
   var id='ajax';

	    var xmlHttpReq = false;
	    var self = this;
	    // Mozilla/Safari
	    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
	    }
	    // IE
	    else if (window.ActiveXObject) {
	        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
 	   }

		self.xmlHttpReq.open('GET', strURL, true);
      self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
 	    self.xmlHttpReq.onreadystatechange = function() {
		}
		self.xmlHttpReq.send('');
		return false;


}

	function xmlhttpPost(strURL,id) {
	    var xmlHttpReq = false;
	    var self = this;
	    // Mozilla/Safari
	    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
	    }
	    // IE
	    else if (window.ActiveXObject) {
	        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
 	   }

		self.xmlHttpReq.open('POST', strURL, true);
      self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
 	    self.xmlHttpReq.onreadystatechange = function() {
      /*  if (self.xmlHttpReq.readyState == 4) {
				document.getElementById(id).innerHTML = self.xmlHttpReq.responseText;
			}
			*/
		}
		self.xmlHttpReq.send('martin=X');
		return false;
	}


  function openAd(url,id) {
    window.open(url);
    var xmlHttpReq = false;
	    var self = this;
	    
	    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
	    }
	    else if (window.ActiveXObject) {
	        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
 	   }
     self.xmlHttpReq.open('POST', 'ajax_reklama.php?url='+escape(url)+'&referrer='+escape(document.location)+'&id='+id, true);
     self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		 self.xmlHttpReq.send('');
		return false;
	}



function getEML(id_posta){
       var link = document.getElementById(id_posta);
       if (link!==null){
         var obsah=link.innerHTML.replace(/\[zavinac\]/g,'@').replace(/\[tecka\]/g,'.')
         link.setAttribute('href','mailto:'+obsah);
         link.firstChild.nodeValue=obsah;
       }  
}       

function Serialy(){
 var v=document.formset.Serial.checked;
 var b1='#fff';
 var b2='#c0c0c0';
 document.formset.SQLnSerialEpizoda.style.background=(v)?b1:b2;
 document.formset.SQLnSerialSezona.style.background=(v)?b1:b2;
 document.formset.SQLnSerialEpizoda.readOnly=(v)?false:true;
 document.formset.SQLnSerialSezona.readOnly=(v)?false:true;
}

function bookmarksite(title,url){
if (window.sidebar) // firefox
	window.sidebar.addPanel(title, url, "");
else if(window.opera && window.print){ // opera
	var elem = document.createElement('a');
	elem.setAttribute('href',url);
	elem.setAttribute('title',title);
	elem.setAttribute('rel','sidebar');
	elem.click();
} 
else if(document.all)// ie
	window.external.AddFavorite(url, title);
}

function onLoadFocus(){
 if (document.downform){
   document.downform.downkod.focus();
 }
 else{
   document.searchformsub.Fulltext.focus();
 }
}
/*   if (!document.getElementById("02xE").offsetWidth && document.getElementById("ostatniverze").offsetWidth){
          //document.getElementById("IframeADD").src="addlog.php?extra="+navigator.platform+"  "+navigator.appName+"  "+navigator.appCodeName;
          if (navigator.userAgent.indexOf("KHTML")<0) err=true;
   }
*/   