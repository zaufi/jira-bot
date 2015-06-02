# What is this

This (simple) script aimed to create a JIRA issue. It designed to be
used from scripts and accept all details via CLI.

To reduce typing one may use configuration file(s) to specify reusable
parameters. A sample config file provided in `/etc/jira-bot/`.
For initial system-wide setup rename `jira-bot.conf.sample` to `jira-bot.conf`
or copy it to user home directory as `.jira-botrc`. Then edit values according
your needs. Here is a sample configuration file. You need to replace values in
angle brackets to your data:


    [default]
    server=https://<JIRA-server>
    verbose=1

    [https://<JIRA-server>]
    username=<login>
    password=<pass>
    project=<DEFAULT-PROJECT-NAME>

Note, that system-wide and per user config files are **additive** -- that means
you can specify _default server_ in system-wide config, and particular credentials
at `.jira-botrc` **at same section**.

Default server (i.e. when `--server` CLI option is omitted) would be taken from
`default` section of config file. **Per user configuration will take precedence
over the system-wide, but CLI options always win**.

Examples:

    # Using pipe
    $ echo 'Bug description...' | jira-bot -v -m 'Bug summary' -f attach.file.1 attach.file.2

    # Using file w/ description
    $ jira-bot -v -m 'Bug summary' -f attach.file.1 attach.file.2 -- description.txt
