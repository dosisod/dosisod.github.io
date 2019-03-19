//gets my last commit

async function get_last() {
	await fetch("https://api.github.com/users/dosisod/events")
		.then(e=>e.json())
		.then(e=>{
			json=e
		})

	html=document.getElementById("recent") //stores html to display

	addspan=(msg, css, app)=>{ //message, css class, append to
		tmp=document.createElement("span")
		tmp.className="bubble "+css
		tmp.innerText=msg

		app.appendChild(tmp)
	}

	last=""
	for (i in json) {
		li=document.createElement("li")

		d=new Date(json[i]["created_at"]) //parse date
		str=d.toString().split(" ").splice(1,2).join(" ")
		if (str!=last) {
			addspan(str, "bubble-fill", li) //create string
		}
		else {
			addspan(str, "bubble-spacer", li) //same indent, just empty
		}
		last=str
		
		addspan(json[i]["repo"]["name"].split("/")[1], "bubble-void", li) //repo name
		
		if (json[i]["type"]=="PushEvent") {
			addspan(json[i]["payload"]["commits"][0]["message"], "bubble-void", li) //message for commit
			html.appendChild(li)
		}
		else if (json[i]["payload"]["ref_type"]=="branch") {
			addspan("new repo", "bubble-fill", li) //is a new commit
			html.appendChild(li)
		}
	}
}