
document.write('<!-- spir.czMonS[370_65788_142763_CPT_243920] -->');//<![CDATA[
_gde_rlilglftdf = new Image(1,1);
_gde_rlilglftdf.src='http://gdecz.hit.gemius.pl/_'+(new Date()).getTime()+'/redot.gif?id=ctTg7c_Zo4mODejqzHlZ5cQLTH6yXvfq0GenmL9Zf7j.Q7/fastid=2305843009233766270/stparam=rlilglftdf';
//]]>

//v2006-04-21 (eolas patch) script made by Internet BillBoard
//v2008-02-19 full parameters extensions 
var bb_Height=100;// vyska
var bb_Width=745; // sirka
var bb_FlashName="ING_veverka_745x100.swf"; //jmeno souboru flashe
var bb_FlashVer=7; // verze flashe
var bb_Wmode="opaque"; //wmode pro flash
var bb_targetstring = "&clickTarget=_blank";
var bb_domain1string = "&domain1=ad2.bbmedia.cz"
var bb_domain2string = "&domain2="+document.domain;

// DALE NEEDITOVAT

var bb_redir='http://go.cz.bbelements.com/please/redirect/15371/1/2/7/!uwi=1280;uhe=800;uce=0;param=242454/243920_1_?';
var bb_url='http://bbcdn.go.cz.bbelements.com/logos/cdn3121/b242454/';

var bb_Swf = bb_url+bb_FlashName+'?clickthru='+escape(bb_redir)+bb_targetstring+bb_domain1string+bb_domain2string+'&clickTAG='+escape(bb_redir)+bb_targetstring+bb_domain1string+bb_domain2string+'&clickTag='+escape(bb_redir)+bb_targetstring+bb_domain1string+bb_domain2string+'&b=12';
var bb_flashakt=0;
var bb_isflash=0;
if(navigator.appVersion.indexOf('MSIE')>=0 && navigator.appVersion.indexOf('Win')>=0) {
 document.writeln('<scr'+'ipt language=VBScript\>');
 document.writeln('on error resume next');
 for(i=3;i<11;i++) document.writeln('if (IsNull(CreateObject("ShockwaveFlash.ShockwaveFlash.'+i+'"))) then dummy=0 else bb_flashakt='+i+' end if');
 document.writeln('</'+'scr'+'ipt\>');
}
if(navigator.plugins && navigator.plugins["Shockwave Flash"]) {
 var flashdesc = navigator.plugins["Shockwave Flash"].description;
 bb_flashakt = parseInt(flashdesc.match(/[!\d]*(\d+)/)[0]);
}

if (bb_flashakt>=bb_FlashVer) {
 var bb_Param="<param name=allowscriptaccess value=always>";
 var bb_Embed="allowscriptaccess=always";
 var bb_Object="";
 document.write("<scr"+"ipt language=JavaScript src=http://go.cz.bbelements.com/bb/bb_flash2.js ></"+"scr"+"ipt>");
} else {
 document.write("<a href='"+bb_redir+"' target='_blank'><img src='http://bbcdn.go.cz.bbelements.com/logos/cdn3121/b242454_4.gif' width="+bb_Width+" height="+bb_Height+" border=0 /></a>");
}
document.write('<!-- spir.czMonE -->');
if((typeof window.BBEBNL).toUpperCase() == "UNDEFINED"){document.write("<SCR"+"IPT language='JavaScript' src='http://bbcdn.go.eu.bbelements.com/js/bbnaut.js'></SCR"+"IPT>");}


