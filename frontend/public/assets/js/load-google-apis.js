// Load config file
fetch('/assets/config.json').then(r => {
  r.json().then(j => {
    console.log('index.html > script > fetch.then > json.then > j', j);

    // Load Google Maps JavaScript API
    if (Object.hasOwnProperty(j, 'googleMapsApiKey')) {
      const mapsKey = j.googleMapsApiKey || '__GOOGLE_MAPS_API_KEY__';

      if (/^__(.*)__$/.test(mapsKey)) {
        console.log('No Google Maps API key set. Skipping Google Maps script load.');
      } else {
        // prettier-ignore
        (g=>{var h,a,k,p='The Google Maps JavaScript API',c='google',l='importLibrary',q='__ib__',m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await(a=m.createElement('script'));e.set('libraries',[...r]+'');for(k in g)e.set(k.replace(/[A-Z]/g,t=>'_'+t[0].toLowerCase()),g[k]);e.set('callback',c+'.maps.'+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+' could not load.'));a.nonce=m.querySelector('script[nonce]')?.nonce||'';m.head.append(a);}));d[l]?console.warn(p+' only loads once. Ignoring:',g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n));})({v:'weekly',key:mapsKey});
      }
    }

    // Load Google Analytics Javascript API
    if (Object.hasOwnProperty(j, 'googleAnalyticsTagId')) {
      const gaTagId = j.googleAnalyticsTagId || '__GOOGLE_ANALYTICS_TAG_ID__';

      if (/^__(.*)__$/.test(gaTagId)) {
        console.log('No GTM ID set. Skipping GTM script load.');
      } else {
        // prettier-ignore
        gtag('js', new Date());
        gtag('config', gaTagId);
      }
    }
  });
});

// Load YouTube Embed API
// prettier-ignore
(_=>{let t=document.createElement('script');t.src='https://www.youtube.com/iframe_api';let f=document.getElementsByTagName('script')[0];f.parentNode.insertBefore(t,f);})();
