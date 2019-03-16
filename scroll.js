//scroll handler

document.body.onwheel=e=>{ //smooth paralax scrolling
	window.scrollBy({
		left: e.deltaY*100,
		behavior: "smooth"
	})
}