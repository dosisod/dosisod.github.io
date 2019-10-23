//gets and parses most recent commits
function recent_commits() {
	fetch("https://api.github.com/users/dosisod/events").then(function(e){return e.json()}).then(function(e){
	json=e

	var html=document.getElementById("recent") //stores html to display

	function addspan(msg, css, app) { //message, css class, append to
		nu("span", {
			"className": "bubble "+css,
			"innerText": msg
		}, app)
	}

	var arr=[]
	for (var i of json) {
		var tmp=new Date(i["created_at"]) //parse date
		var date=tmp.toString().split(" ").splice(1,2).join(" ")

		var repo=i["repo"]["name"].split("/")[1]

		//normal push, loop through commits
		if (i["type"]=="PushEvent") {
			for (j of i["payload"]["commits"]) {
				arr.push({
					"date": date,
					"commit": j["message"].replace(/\n/g, " "),
					"repo": repo
				})
			}
		}
		//new repo added
		else if (i["type"]=="CreateEvent"&&i["payload"]["ref"]==null) {
			arr.push({
				"date": date,
				"new": "new repo",
				"repo": repo
			})
		}
		else if (i["type"]=="PullRequestEvent") {
			if (i["payload"]["pull_request"]["state"]=="closed") {
				arr.push({
					"date": date,
					"new": "new PR",
					"repo": repo
				})
			}
		}
	}

	var last=""
	for (var i of arr) {
		var li=nu("li", {"className": "recent_commit"})

		if (i["date"]!=last) {
			addspan(i["date"], "bubble-fill", li) //create string
		}
		else {
			addspan(i["date"], "bubble-spacer", li) //same indent, just empty
		}
		last=i["date"]

		addspan(i["repo"], "bubble-void", li) //repo name

		if (i["commit"]) {
			addspan(i["commit"], "bubble-void", li) //message for commit
			html.appendChild(li)
		}
		else if (i["new"]) {
			addspan(i["new"], "bubble-fill", li) //this is a PR or a new repo
			html.appendChild(li)
		}
	}})
}