// import "node_modules/core-js/client/shim.min.js";

/**
 * you can configure some zone flags which can disable zone interception for some
 * asynchronous activities to improve startup performance - use these options only
 * if you know what you are doing as it could result in hard to trace down bugs.
 */
(window as any).__Zone_disable_requestAnimationFrame = true; // disable patch requestAnimationFrame
(window as any).__Zone_disable_on_property = true; // disable patch onProperty such as onclick
(window as any).__zone_symbol__UNPATCHED_EVENTS = ["scroll", "mousemove"]; // disable patch specified eventNames

/**
 * in Edge developer tools, the addEventListener will also be wrapped by zone.js
 * with the following flag, it will bypass `zone.js` patch for Edge.
 */
(window as any).__Zone_enable_cross_context_check = true;


/***************************************************************************************************
 * Zone JS is required by default for Angular itself.
 */
import "node_modules/zone.js/bundles/zone.umd.js"; // Included with Angular CLI.
