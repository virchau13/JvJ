let ipaddr = '192.168.1.81';

window.onerror = function(){ alert('error!') };

function graph(obj){
	document.getElementById('cloud-container').innerHTML = `<svg id="wordcloud" version="1.1" baseProfile="full" width="${screen.availWidth}" height="${screen.availHeight - 100}" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="0" x2="${screen.availWidth}" y2="0" style="stroke: #ffffff; stroke-width: 1"></line>
	<line x1="0" y1="0" x2="0" y2="${screen.availHeight-100}" style="stroke: #ffffff; stroke-width: 1"></line>
	<line x1="${screen.availWidth}" y1="${screen.availHeight-100}" x2="0" y2="${screen.availHeight-100}" style="stroke: #ffffff; stroke-width: 1"></line>
	<line x1="${screen.availWidth}" y1="${screen.availHeight}" x2="${screen.availWidth}" y2="0" style="stroke: #ffffff; stroke-width: 1"></line></svg>`
	let fqdist = Object.entries(obj).sort((a,b)=>b[1]-a[1]).slice(0, 50 + 1).reduce((obj, [k, v]) => ({ ...obj, [k]: v }), {});
	let svg = document.getElementById('wordcloud');
	let el;
	let points;
	let intersects;
	let max = Math.max.apply(null, Object.values(fqdist));
	function place(elm, rendered){
		elm.setAttributeNS(null, 'x', Math.floor(Math.random() * screen.availWidth));
		elm.setAttributeNS(null, 'y', Math.floor(Math.random() * screen.availHeight));
		// if(rendered) { console.log('rendered'); if(svg.getIntersectionList(el.getBBox(), null).length > 0){ console.log('collision'); /* collision! */ setxy(elm, true) } };
		// if(elm.innerHTML.getAttribute('fontsize'))
	}
	for(let w in fqdist){
		el = Object.assign(document.createElementNS("http://www.w3.org/2000/svg", "text"), {innerHTML: w});
		el.setAttributeNS(null, 'fontsize', fqdist[w]/max * 40);
		place(el);
		el.style.fontSize = fqdist[w]/max * 40 + 'px';
		svg.appendChild(el);
		if(svg.getIntersectionList(el.getBBox(), null).length > 1){
			place(el, true);
		}
	}
}

document.addEventListener("DOMContentLoaded", () => {
	// searchbar controls
	let searchbar = document.getElementById("search");
	searchbar.addEventListener("keypress",(e) => {
		if(e.which === 13){
			// make loading bar
			document.getElementById('searchbar').innerHTML = `<div id="loader" style="border: 8px solid #f3f3f3; 
			border-top: 8px solid #555;
			border-radius: 50%;
			width: 50px;
			height: 50px;
			margin-left: 30%;
			animation: spin 2s linear infinite;"></div><br><p> Loading search results... </p>`
			// GET data from server for rendering
			fetch("http://" + ipaddr + ":5000/scrape?querystring=" + e.target.value)
			.then((data) => data.json())
			.then((data) => {document.body.removeChild(document.getElementById('searchbar')); console.log(data); graph(data)});
		}
	})
})


function collision(el, bbox, svg){

}