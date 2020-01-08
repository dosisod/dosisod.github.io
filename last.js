function recent_commits() {
	fetch("https://api.github.com/users/dosisod/events")
		.then(function(e) { return e.json() })
		.then(function(e) {
			parse_events(e)
		})
}

function parse_events(events) {
	var commits=[]
	for (const git_event of events) {
		const date_obj=new Date(git_event["created_at"])
		const date=date_obj.toString()
			.split(" ")
			.splice(1, 2)
			.join(" ")

		const repo=git_event["repo"]["name"].split("/")[1]

		if (git_event["type"]=="PushEvent") {
			for (const commit of git_event["payload"]["commits"].reverse()) {
				commits.push({
					"date": date,
					"commit_msg": commit["message"].replace(/\n/g, " "),
					"repo": repo
				})
			}
		}
		else if (git_event["type"]=="CreateEvent" && git_event["payload"]["ref"]==null) {
			commits.push({
				"date": date,
				"new": "new repo",
				"repo": repo
			})
		}
		else if (git_event["type"]=="PullRequestEvent") {
			if (git_event["payload"]["pull_request"]["state"]=="closed") {
				commits.push({
					"date": date,
					"new": "new PR",
					"repo": repo
				})
			}
		}
	}

	var last_date=""
	for (const commit of commits) {
		const li=nu("li", {"className": "recent-commit"})

		let classname="bubble-fill"
		if (commit["date"]==last_date) classname="bubble-spacer"
		addspan(commit["data"], classname, li)

		last_date=commit["date"]

		classname="bubble-void"
		addspan(commit["repo"], classname, li)

		if (commit["commit_msg"] || commit["new"]) {
			if (commit["new"]) classname="bubble-fill"

			addspan(
				commit["commit_msg"] || commit["new"],
				classname,
				li
			)
			nu("recent").appendChild(li)
		}
	}
}

function addspan(msg, classname, node) {
	nu("span", {
		"className": "bubble "+classname,
		"innerText": msg
	}, node)
}