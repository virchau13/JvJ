document.addEventListener("DOMContentLoaded", () => {
	let searchbar = document.getElementById("search");
	searchbar.addEventListener("keypress",(e) => {
		if(e.which === 13)
			console.log(e.target.value);
		// GET data from server for rendering
	})

	let fqdist = {
		lol: 23,
		i: 44,
		am: 55,
		ok: 23,
		so: 10,
		yeah: 1
	};
	let ypos = 200;
	let el;
	let max = Math.max.apply(null, Object.values(fqdist));
	for(let w in fqdist){
		el = Object.assign(document.createElementNS("http://www.w3.org/2000/svg", "text"), {innerHTML: w});
		let wantedPos = {x: Math.floor(Math.random() * 500), y: Math.floor(Math.random() * 500)};
		el.setAttributeNS(null, 'fontsize', fqdist[w]/max * 40);
		el.setAttributeNS(null, 'x', wantedPos.x);
		el.setAttributeNS(null, 'y', wantedPos.y);
		el.style.fontSize = fqdist[w]/max * 40 + 'px';
		document.getElementById('wordcloud').appendChild(el);
		ypos += el.getBBox().height + 5;
		console.log(ypos, w);
	}

})
