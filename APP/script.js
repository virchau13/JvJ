let ipaddr = /* Enter IP address here. e.g. */ '192.168.1.81';

document.addEventListener("DOMContentLoaded", () => {
	let searchbar = document.getElementById("search");
	searchbar.addEventListener("keypress",(e) => {
		if(e.which === 13){
			// GET data from server for rendering
			document.getElementById('cloud-container').innerHTML = `
			<svg id="wordcloud" version="1.1" id= baseProfile="full" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">
			</svg>
			`;
			fetch("http://" + ipaddr + ":5000/scrape?querystring=" + e.target.value)
			.then((data) => data.json())
			.then((data) => graph(data))

	}})

	function graph(fqdist){
		let ypos = 200;
		let el;
		let max = Math.max.apply(null, Object.values(fqdist));
		for(let w in fqdist){
			el = Object.assign(document.createElementNS("http://www.w3.org/2000/svg", "text"), {innerHTML: w});
			let wantedPos = {x: Math.floor(Math.random() * 1000), y: Math.floor(Math.random() * 1000)};
			el.setAttributeNS(null, 'fontsize', fqdist[w]/max * 40);
			el.setAttributeNS(null, 'x', wantedPos.x);
			el.setAttributeNS(null, 'y', wantedPos.y);
			el.style.fontSize = fqdist[w]/max * 40 + 'px';
			document.getElementById('wordcloud').appendChild(el);
			ypos += el.getBBox().height + 5;
			console.log(ypos, w);
		}
	}

})
