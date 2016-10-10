Simple script to clone all (or some) repos in one or multiple Github Orgs. Run with `--help` to see options.


Examples
--------

* Clone all the repos in an Org, using user/pass: `python clone_org.py --user=name --password=pass Org`
* Clone all the repos in an Org, using person access token (easier, if you have 2 factor auth): `python clone_org.py --token=token Org`
* Clone all repos in multiple Orgs, excluding 2 specific repos, all repos with "test" in the name, and all repos beginning with "py": `python clone_org.py --token=token --exclude=not-this-one,or-this-one --exclude-regex='^py|test' Org`
