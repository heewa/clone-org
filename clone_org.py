#!/usr/bin/env python
from subprocess import call, check_output
from sys import exit, stderr
from os import path
import shlex
import re

from github import Github


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='Usage: %prog [options] org [org2...]')

    parser.add_option('', '--token', dest='token',
                      help='Github API token')
    parser.add_option('', '--user', dest='user',
                      help='Github user')
    parser.add_option('', '--password', dest='password',
                      help='Github password')

    parser.add_option('', '--type', dest='type', default='sources',
                      help='Repo type (all, public, private, forks, sources, '
                           'member), default=sources')
    parser.add_option('', '--https', dest='https',
                      action='store_true', default=False,
                      help='Clone with https url instead of ssh')

    parser.add_option('', '--git-args', dest='git_args',
                      help='Additional args to "git" before "clone"')
    parser.add_option('', '--clone-args', dest='clone_args',
                      help='Additional args to "git clone"')
    parser.add_option('', '--git', dest='git',
                      help='Path to git executable')

    parser.add_option('', '--exclude', dest='exclude',
                      help='Comma separated list of repo names to exclude')
    parser.add_option('', '--exclude-regex', dest='exclude_regex',
                      help='Regex pattern for repo names to exlucde')

    parser.add_option('-t', '--test', dest='test',
                      action='store_true', default=False,
                      help='Test run, don\'t actually clone repos.')
    parser.add_option('-s', '--skip-existing', dest='skip_existing',
                      action='store_true', default=False,
                      help='Skip existing repo directories')

    options, orgs = parser.parse_args()

    if not orgs:
        exit('Need to give at least one org to clone repos from')

    if options.token:
        ghub = Github(options.token)
    elif options.user and options.password:
        ghub = Github(options.user, options.password)
    else:
        exit('Need to give either a token or user+password')

    git_path = options.git or check_output(['/usr/bin/which', 'git']).strip()

    clone_args = [git_path]
    if options.git_args:
        clone_args += shlex.split(options.git_args)
    clone_args.append('clone')
    if options.clone_args:
        clone_args += shlex.split(options.clone_args)

    excludes = [
        repo.strip()
        for repo in (options.exclude or '').split(',')
        if repo.strip()
    ]
    exclude_re = options.exclude_regex and re.compile(
        options.exclude_regex)

    for org_name in orgs:
        org = ghub.get_organization(org_name)

        repos = [
            repo
            for repo in org.get_repos(options.type)
            if (
                (not excludes or repo.name not in excludes) and
                (not exclude_re or not exclude_re.search(repo.name)) and
                (not options.skip_existing or not path.exists(repo.name)))
        ]

        for repo in repos:
            repo_url = options.https and repo.clone_url or repo.ssh_url
            print repo_url

            if not options.test:
                clone_ret = call(clone_args + [repo_url])
                if clone_ret != 0:
                    exit('Failed to clone repo %s' % repo.name)
