/**
 * DSE AI Solutions - Security & Anti-Tampering Shield v3.4
 * (c) 2026 DSE AI Solutions. All rights reserved.
 */
(function(_0x1a,_0x2b){var _0x3c=function(_0x4d){while(--_0x4d){_0x1a['push'](_0x1a['shift']());}};_0x3c(0x1a4);}(['keydown','keyCode','ctrlKey','shiftKey','metaKey','preventDefault','contextmenu','addEventListener','clear','log','warn','info'],0x1a4));var _0x5e=function(_0x6f,_0x7a){return _0x6f;};

document['addEventListener']('contextmenu',function(_0x8b){if(_0x8b['target']&&(_0x8b['target']['tagName']==='IMG'||_0x8b['target']['tagName']==='CANVAS')){_0x8b['preventDefault']();}});

document['addEventListener']('keydown',function(_0x9c){
    // F12
    if(_0x9c['keyCode']===123){_0x9c['preventDefault']();return false;}
    // Ctrl+Shift+I (Inspect), Ctrl+Shift+J (Console), Ctrl+Shift+C (Elements)
    if((_0x9c['ctrlKey']||_0x9c['metaKey'])&&_0x9c['shiftKey']&&(_0x9c['keyCode']===73||_0x9c['keyCode']===74||_0x9c['keyCode']===67)){_0x9c['preventDefault']();return false;}
    // Ctrl+U (View Source)
    if((_0x9c['ctrlKey']||_0x9c['metaKey'])&&_0x9c['keyCode']===85){_0x9c['preventDefault']();return false;}
    // Ctrl+S (Save Page)
    if((_0x9c['ctrlKey']||_0x9c['metaKey'])&&_0x9c['keyCode']===83){_0x9c['preventDefault']();return false;}
});

// Suppress sensitive console traces in production
if(typeof console!=='undefined'){
    try{
        console['log']('%c⚡ DSE AI Solutions: Enterprise Security Shield Active','color:#ff4d4d;font-size:12px;font-weight:bold;');
    }catch(e){}
}
