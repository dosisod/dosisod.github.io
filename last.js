//gets my last commit

function get_last() {
	/* keep this commented out untill it is fully done
	fetch("https://api.github.com/users/dosisod/events?per_page=1")
		.then(e=>e.text())
		.then(e=>{
			console.log(e)
		})
	*/

	//string from above code instead of running it each time
	str=`
	[
	  {
	    "id": "9254286412",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 170422639,
	      "name": "dosisod/dosisod.github.io",
	      "url": "https://api.github.com/repos/dosisod/dosisod.github.io"
	    },
	    "payload": {
	      "push_id": 3406200345,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "82c828e982419d9b3554816b9da35f19a192b422",
	      "before": "c5a7ebae881309ae08fb345d3a6543c1f5e62af6",
	      "commits": [
	        {
	          "sha": "82c828e982419d9b3554816b9da35f19a192b422",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added transitions and paralax",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/dosisod.github.io/commits/82c828e982419d9b3554816b9da35f19a192b422"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-15T22:54:56Z"
	  },
	  {
	    "id": "9247436612",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 159279896,
	      "name": "dosisod/jsxl",
	      "url": "https://api.github.com/repos/dosisod/jsxl"
	    },
	    "payload": {
	      "push_id": 3402586322,
	      "size": 3,
	      "distinct_size": 3,
	      "ref": "refs/heads/master",
	      "head": "b7cb7a6d1b925c5fe962bf86b16e289f012f2598",
	      "before": "c9fbf217b2f6831ef97a9012c72250bbe8f75cf3",
	      "commits": [
	        {
	          "sha": "f8b0e2bedfe1c6e527bc99ff70857d6b9b92e775",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added better auto bracketting",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/f8b0e2bedfe1c6e527bc99ff70857d6b9b92e775"
	        },
	        {
	          "sha": "799dd11ba05c4aa558d23181f4be775f9ea49da1",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "using e.key now",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/799dd11ba05c4aa558d23181f4be775f9ea49da1"
	        },
	        {
	          "sha": "b7cb7a6d1b925c5fe962bf86b16e289f012f2598",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "moved onkeydown, cleaned up vars",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/b7cb7a6d1b925c5fe962bf86b16e289f012f2598"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-15T00:46:32Z"
	  },
	  {
	    "id": "9239991599",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 159279896,
	      "name": "dosisod/jsxl",
	      "url": "https://api.github.com/repos/dosisod/jsxl"
	    },
	    "payload": {
	      "push_id": 3398689290,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "c9fbf217b2f6831ef97a9012c72250bbe8f75cf3",
	      "before": "b2f4f2e041ee8aac02f8e103ee59a78896b534b8",
	      "commits": [
	        {
	          "sha": "c9fbf217b2f6831ef97a9012c72250bbe8f75cf3",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "enter now keeps indents",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/c9fbf217b2f6831ef97a9012c72250bbe8f75cf3"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-14T04:08:32Z"
	  },
	  {
	    "id": "9239451639",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 159279896,
	      "name": "dosisod/jsxl",
	      "url": "https://api.github.com/repos/dosisod/jsxl"
	    },
	    "payload": {
	      "push_id": 3398392706,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "b2f4f2e041ee8aac02f8e103ee59a78896b534b8",
	      "before": "3e760f624abff09f70849bfe131b05889e935730",
	      "commits": [
	        {
	          "sha": "b2f4f2e041ee8aac02f8e103ee59a78896b534b8",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added better syntaxing",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/b2f4f2e041ee8aac02f8e103ee59a78896b534b8"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-14T01:33:13Z"
	  },
	  {
	    "id": "9232111334",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 154909791,
	      "name": "dosisod/wasjs",
	      "url": "https://api.github.com/repos/dosisod/wasjs"
	    },
	    "payload": {
	      "push_id": 3394564965,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "9aace752150837d1156af9951be2e18f4d621590",
	      "before": "88765091ec84f7fdcb226ceed53ace8a86a1b1f1",
	      "commits": [
	        {
	          "sha": "9aace752150837d1156af9951be2e18f4d621590",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "updated comments",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/wasjs/commits/9aace752150837d1156af9951be2e18f4d621590"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-13T05:44:50Z"
	  },
	  {
	    "id": "9232086277",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 154909791,
	      "name": "dosisod/wasjs",
	      "url": "https://api.github.com/repos/dosisod/wasjs"
	    },
	    "payload": {
	      "push_id": 3394552485,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "88765091ec84f7fdcb226ceed53ace8a86a1b1f1",
	      "before": "c41bc3a195d3711e38586aac8b301cf004e558b6",
	      "commits": [
	        {
	          "sha": "88765091ec84f7fdcb226ceed53ace8a86a1b1f1",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "fixed wording",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/wasjs/commits/88765091ec84f7fdcb226ceed53ace8a86a1b1f1"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-13T05:38:08Z"
	  },
	  {
	    "id": "9232058752",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 159279896,
	      "name": "dosisod/jsxl",
	      "url": "https://api.github.com/repos/dosisod/jsxl"
	    },
	    "payload": {
	      "push_id": 3394537537,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "3e760f624abff09f70849bfe131b05889e935730",
	      "before": "c8d4d18675aeb04de3a907d4269773c6e86abb27",
	      "commits": [
	        {
	          "sha": "3e760f624abff09f70849bfe131b05889e935730",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added tab preventions and fixed function execution",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/3e760f624abff09f70849bfe131b05889e935730"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-13T05:30:08Z"
	  },
	  {
	    "id": "9223775449",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 150826660,
	      "name": "dosisod/music",
	      "url": "https://api.github.com/repos/dosisod/music"
	    },
	    "payload": {
	      "push_id": 3390216078,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "9544fcb9b032964aebf1b88f43bed85439c3b674",
	      "before": "96a666c3d5c20245b728c866f4c999753b90b609",
	      "commits": [
	        {
	          "sha": "9544fcb9b032964aebf1b88f43bed85439c3b674",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "cleaned up brackets",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/music/commits/9544fcb9b032964aebf1b88f43bed85439c3b674"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-12T05:14:14Z"
	  },
	  {
	    "id": "9223762641",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 159279896,
	      "name": "dosisod/jsxl",
	      "url": "https://api.github.com/repos/dosisod/jsxl"
	    },
	    "payload": {
	      "push_id": 3390208993,
	      "size": 2,
	      "distinct_size": 2,
	      "ref": "refs/heads/master",
	      "head": "c8d4d18675aeb04de3a907d4269773c6e86abb27",
	      "before": "f05f29eea08e45ebcc062f0fb4bb771729e4edd6",
	      "commits": [
	        {
	          "sha": "fcdaa4b8f6e33d1c04e3a62340aab23ccbb02b11",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "cleaned up code",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/fcdaa4b8f6e33d1c04e3a62340aab23ccbb02b11"
	        },
	        {
	          "sha": "c8d4d18675aeb04de3a907d4269773c6e86abb27",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "optimized init",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/jsxl/commits/c8d4d18675aeb04de3a907d4269773c6e86abb27"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-12T05:09:55Z"
	  },
	  {
	    "id": "9223725908",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3390189543,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "06bd5220cb3f66dda368bf567cf5f448fd76e54e",
	      "before": "9265f689a6603d427696b20ce4f6c8190dc24482",
	      "commits": [
	        {
	          "sha": "06bd5220cb3f66dda368bf567cf5f448fd76e54e",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "updated readme",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/06bd5220cb3f66dda368bf567cf5f448fd76e54e"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-12T04:58:27Z"
	  },
	  {
	    "id": "9214926951",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 148860884,
	      "name": "dosisod/EZWS",
	      "url": "https://api.github.com/repos/dosisod/EZWS"
	    },
	    "payload": {
	      "push_id": 3385583823,
	      "size": 3,
	      "distinct_size": 3,
	      "ref": "refs/heads/master",
	      "head": "ea48d439462fdad2021db0ff36b54603ac88f08a",
	      "before": "57bb5e0fab480b7896061216139540f9c6ea379b",
	      "commits": [
	        {
	          "sha": "6b11602d2359623d7b3b6ae6562dca75b01b41e5",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "fixed broken links",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/EZWS/commits/6b11602d2359623d7b3b6ae6562dca75b01b41e5"
	        },
	        {
	          "sha": "50cfa7f642a9ff9fa5b0e5187fbfbd486cfa9f13",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "fixed broken links",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/EZWS/commits/50cfa7f642a9ff9fa5b0e5187fbfbd486cfa9f13"
	        },
	        {
	          "sha": "ea48d439462fdad2021db0ff36b54603ac88f08a",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added check to docs",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/EZWS/commits/ea48d439462fdad2021db0ff36b54603ac88f08a"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-10T23:51:11Z"
	  },
	  {
	    "id": "9213028395",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3384371218,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "9265f689a6603d427696b20ce4f6c8190dc24482",
	      "before": "e0f6b6426cd2bc7c98ce38c655bb86cc4f554a72",
	      "commits": [
	        {
	          "sha": "9265f689a6603d427696b20ce4f6c8190dc24482",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added optimizations from 2048.min.js",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/9265f689a6603d427696b20ce4f6c8190dc24482"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-10T07:55:52Z"
	  },
	  {
	    "id": "9212802000",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3384224524,
	      "size": 2,
	      "distinct_size": 2,
	      "ref": "refs/heads/master",
	      "head": "e0f6b6426cd2bc7c98ce38c655bb86cc4f554a72",
	      "before": "d39d407ea318c86adc52db772907c64ab08bf7b3",
	      "commits": [
	        {
	          "sha": "36f7473e21ac619e18b5dfcf7fcd441f21f3b0a4",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added win message",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/36f7473e21ac619e18b5dfcf7fcd441f21f3b0a4"
	        },
	        {
	          "sha": "e0f6b6426cd2bc7c98ce38c655bb86cc4f554a72",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "minified 2048.js",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/e0f6b6426cd2bc7c98ce38c655bb86cc4f554a72"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-10T05:11:04Z"
	  },
	  {
	    "id": "9209874020",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3382372841,
	      "size": 2,
	      "distinct_size": 2,
	      "ref": "refs/heads/master",
	      "head": "d39d407ea318c86adc52db772907c64ab08bf7b3",
	      "before": "11d916a2166ef90a58ab82c7698e28513fd28a4e",
	      "commits": [
	        {
	          "sha": "fbfd72aac21b8ba08a46697edbf10df2854c787b",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "made colors nicer",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/fbfd72aac21b8ba08a46697edbf10df2854c787b"
	        },
	        {
	          "sha": "d39d407ea318c86adc52db772907c64ab08bf7b3",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added death logic",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/d39d407ea318c86adc52db772907c64ab08bf7b3"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-09T00:12:41Z"
	  },
	  {
	    "id": "9204135975",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3379402949,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "11d916a2166ef90a58ab82c7698e28513fd28a4e",
	      "before": "b233578b7a360cdb2401cdeef08297a070d53211",
	      "commits": [
	        {
	          "sha": "11d916a2166ef90a58ab82c7698e28513fd28a4e",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "finished basic structure",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/11d916a2166ef90a58ab82c7698e28513fd28a4e"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-08T06:05:08Z"
	  },
	  {
	    "id": "9204032270",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3379346960,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "b233578b7a360cdb2401cdeef08297a070d53211",
	      "before": "0cd12211cd59fa034e1c54883787d2c2767e1aa9",
	      "commits": [
	        {
	          "sha": "b233578b7a360cdb2401cdeef08297a070d53211",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "can move in all directions now",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/b233578b7a360cdb2401cdeef08297a070d53211"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-08T05:33:49Z"
	  },
	  {
	    "id": "9203408962",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3379002767,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "0cd12211cd59fa034e1c54883787d2c2767e1aa9",
	      "before": "42b178559f1d3ee37214edee370cff5bd32fe2b0",
	      "commits": [
	        {
	          "sha": "0cd12211cd59fa034e1c54883787d2c2767e1aa9",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "fixed left+right moving",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/0cd12211cd59fa034e1c54883787d2c2767e1aa9"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-08T02:20:14Z"
	  },
	  {
	    "id": "9196099715",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3375201098,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "42b178559f1d3ee37214edee370cff5bd32fe2b0",
	      "before": "7205167d0548546658523bf0d601eb58bf5dae98",
	      "commits": [
	        {
	          "sha": "42b178559f1d3ee37214edee370cff5bd32fe2b0",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "fixed array rendering",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/42b178559f1d3ee37214edee370cff5bd32fe2b0"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-07T05:40:14Z"
	  },
	  {
	    "id": "9188086448",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 174038390,
	      "name": "dosisod/ezurl",
	      "url": "https://api.github.com/repos/dosisod/ezurl"
	    },
	    "payload": {
	      "push_id": 3371023440,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "731335f76bb7d6c1129e25a9d4731d2f4310c8f7",
	      "before": "481551ae82cebf5ab4963b9207515a33b0dbed04",
	      "commits": [
	        {
	          "sha": "731335f76bb7d6c1129e25a9d4731d2f4310c8f7",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added ezws class",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/ezurl/commits/731335f76bb7d6c1129e25a9d4731d2f4310c8f7"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-06T06:02:26Z"
	  },
	  {
	    "id": "9186718380",
	    "type": "CreateEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 174038390,
	      "name": "dosisod/ezurl",
	      "url": "https://api.github.com/repos/dosisod/ezurl"
	    },
	    "payload": {
	      "ref": "master",
	      "ref_type": "branch",
	      "master_branch": "master",
	      "description": "Easy URL: Use EZWS config files to scrape files off URLs",
	      "pusher_type": "user"
	    },
	    "public": true,
	    "created_at": "2019-03-05T23:50:55Z"
	  },
	  {
	    "id": "9186718286",
	    "type": "CreateEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 174038390,
	      "name": "dosisod/ezurl",
	      "url": "https://api.github.com/repos/dosisod/ezurl"
	    },
	    "payload": {
	      "ref": null,
	      "ref_type": "repository",
	      "master_branch": "master",
	      "description": "Easy URL: Use EZWS config files to scrape files off URLs",
	      "pusher_type": "user"
	    },
	    "public": true,
	    "created_at": "2019-03-05T23:50:54Z"
	  },
	  {
	    "id": "9179339911",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3366434395,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "7205167d0548546658523bf0d601eb58bf5dae98",
	      "before": "6b87684d7a3462f97f4ced50fb37aa3c3a89c3a6",
	      "commits": [
	        {
	          "sha": "7205167d0548546658523bf0d601eb58bf5dae98",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "started on 2048",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/7205167d0548546658523bf0d601eb58bf5dae98"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-05T02:46:26Z"
	  },
	  {
	    "id": "9171933076",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3362592372,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "6b87684d7a3462f97f4ced50fb37aa3c3a89c3a6",
	      "before": "1b46c8039a1dda2a0fd0a8c471c1531d6c079237",
	      "commits": [
	        {
	          "sha": "6b87684d7a3462f97f4ced50fb37aa3c3a89c3a6",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added instructions to README",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/6b87684d7a3462f97f4ced50fb37aa3c3a89c3a6"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-04T04:33:42Z"
	  },
	  {
	    "id": "9169154762",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "push_id": 3360888854,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "1b46c8039a1dda2a0fd0a8c471c1531d6c079237",
	      "before": "f78604a03d748d12a9291228378b27bb0cf7b9e6",
	      "commits": [
	        {
	          "sha": "1b46c8039a1dda2a0fd0a8c471c1531d6c079237",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added snake",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/concave/commits/1b46c8039a1dda2a0fd0a8c471c1531d6c079237"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-03T06:46:58Z"
	  },
	  {
	    "id": "9169115227",
	    "type": "CreateEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "ref": "master",
	      "ref_type": "branch",
	      "master_branch": "master",
	      "description": "Console-injectable games using JS and HTML5 canvas",
	      "pusher_type": "user"
	    },
	    "public": true,
	    "created_at": "2019-03-03T06:18:43Z"
	  },
	  {
	    "id": "9169115199",
	    "type": "CreateEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 173538606,
	      "name": "dosisod/concave",
	      "url": "https://api.github.com/repos/dosisod/concave"
	    },
	    "payload": {
	      "ref": null,
	      "ref_type": "repository",
	      "master_branch": "master",
	      "description": "Console-injectable games using JS and HTML5 canvas",
	      "pusher_type": "user"
	    },
	    "public": true,
	    "created_at": "2019-03-03T06:18:42Z"
	  },
	  {
	    "id": "9165632695",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 153399773,
	      "name": "dosisod/QUI",
	      "url": "https://api.github.com/repos/dosisod/QUI"
	    },
	    "payload": {
	      "push_id": 3358708382,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "1265bb5e68cf824f43514410d05ddaaf4c9bbd08",
	      "before": "4a57ca274ba8cea010136b76494aa4f7aada62e4",
	      "commits": [
	        {
	          "sha": "1265bb5e68cf824f43514410d05ddaaf4c9bbd08",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "reduced code",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/QUI/commits/1265bb5e68cf824f43514410d05ddaaf4c9bbd08"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-01T22:23:03Z"
	  },
	  {
	    "id": "9160149664",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 148860884,
	      "name": "dosisod/EZWS",
	      "url": "https://api.github.com/repos/dosisod/EZWS"
	    },
	    "payload": {
	      "push_id": 3355862638,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "57bb5e0fab480b7896061216139540f9c6ea379b",
	      "before": "5dae026ef61e7ad37e9593639428b7719ac93181",
	      "commits": [
	        {
	          "sha": "57bb5e0fab480b7896061216139540f9c6ea379b",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added self.raw to docs",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/EZWS/commits/57bb5e0fab480b7896061216139540f9c6ea379b"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-01T06:10:31Z"
	  },
	  {
	    "id": "9160111988",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 148860884,
	      "name": "dosisod/EZWS",
	      "url": "https://api.github.com/repos/dosisod/EZWS"
	    },
	    "payload": {
	      "push_id": 3355842212,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "5dae026ef61e7ad37e9593639428b7719ac93181",
	      "before": "fda80adc05d792dc0ccffa9db2768445238f8ba4",
	      "commits": [
	        {
	          "sha": "5dae026ef61e7ad37e9593639428b7719ac93181",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added xpath to docs",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/EZWS/commits/5dae026ef61e7ad37e9593639428b7719ac93181"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-03-01T06:00:11Z"
	  },
	  {
	    "id": "9151746994",
	    "type": "PushEvent",
	    "actor": {
	      "id": 39638017,
	      "login": "dosisod",
	      "display_login": "dosisod",
	      "gravatar_id": "",
	      "url": "https://api.github.com/users/dosisod",
	      "avatar_url": "https://avatars.githubusercontent.com/u/39638017?"
	    },
	    "repo": {
	      "id": 148860884,
	      "name": "dosisod/EZWS",
	      "url": "https://api.github.com/repos/dosisod/EZWS"
	    },
	    "payload": {
	      "push_id": 3351461783,
	      "size": 1,
	      "distinct_size": 1,
	      "ref": "refs/heads/master",
	      "head": "fda80adc05d792dc0ccffa9db2768445238f8ba4",
	      "before": "67b8d9f88628e68727a20451c4f250d7a72faa3d",
	      "commits": [
	        {
	          "sha": "fda80adc05d792dc0ccffa9db2768445238f8ba4",
	          "author": {
	            "email": "39638017+dosisod@users.noreply.github.com",
	            "name": "dosisod"
	          },
	          "message": "added ua to docs",
	          "distinct": true,
	          "url": "https://api.github.com/repos/dosisod/EZWS/commits/fda80adc05d792dc0ccffa9db2768445238f8ba4"
	        }
	      ]
	    },
	    "public": true,
	    "created_at": "2019-02-28T03:56:45Z"
	  }
	]
	`
	json=JSON.parse(str)
	html=document.getElementById("recent") //stores html to display

	addspan=(msg, css, app)=>{ //message, css class, append to
		tmp=document.createElement("span")
		tmp.className+="bubble "
		tmp.className+=css
		console.log(tmp.className)
		tmp.innerText=msg

		app.appendChild(tmp)
	}
	
	for (item of json) {
		li=document.createElement("li")

		d=new Date(item["created_at"]) //parse date
		addspan(d.toString().split(" ").splice(1,2).join(" "), "bubble-fill", li) //create string
		
		addspan(item["repo"]["name"].split("/")[1], "bubble-void", li) //repo name
		
		if (item["type"]=="PushEvent") {
			addspan(item["payload"]["commits"][0]["message"], "bubble-void", li) //message for commit
		}
		else {
			addspan("new repo", "bubble-fill", li) //is a new commit
		}
		html.appendChild(li)
	}
}