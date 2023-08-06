# rpm-s3

[![Build Status](https://travis-ci.com/voronenko/rpm-s3.svg?branch=master)](https://travis-ci.com/voronenko/rpm-s3)

This small tool allows you to maintain YUM repositories of RPM packages on S3. The code is largely derived from [s3yum-updater](https://github.com/rockpack/s3yum-updater).

The advantage of this tool is that it does not need a full copy of the repo to operate. Just give it the new package to add, and it will just update the repodata metadata, and upload the given rpm file.

If you're looking for the same kind of tool, but for APT repositories, I can recommend [deb-s3](https://github.com/krobertson/deb-s3).

## Requirements

1. You have python installed (2.6+).

1. You have your S3 credentials available in the `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` environment variables:

        export AWS_ACCESS_KEY="key"
        export AWS_SECRET_KEY="secret"

## Installation

From source:   `git clone https://github.com/<current-owner-or-organization>/rpm-s3 `

Example:

```sh
    git clone https://github.com/crohr/rpm-s3 
```    

## Usage

Let's say I want to add a `my-app-1.0.0.x86_64.rpm` package to a yum repo hosted in the `yummy-yummy` S3 bucket, at the path `centos/6`:

    ./rpm-s3 -b yummy-yummy -p "centos/6" my-app-1.0.0.x86_64.rpm

## Testing

Use the provided `/test/test.sh` script:

    vagrant up
    vagrant ssh
    AWS_ACCESS_KEY=xx AWS_SECRET_KET=yy BUCKET=zz ./test/test.sh

Also:

    ./rpm-s3 -b s3-bucket -p "centos/6" --sign my-app-1.0.0.x86_64.rpm

    echo "[myrepo]
    name = This is my repo
    baseurl = https://s3.amazonaws.com/yummy-yummy/centos/6" > /etc/yum.repos.d/myrepo.repo

    yum makecache --disablerepo=* --enablerepo=myrepo

    yum install --nogpgcheck my-app

## Troubleshooting

### Requirements if you want to sign packages

Have a gnupg key ready in your keychain at `~/.gnupg`. You can list existing secret keys with `gpg --list-secret-keys`

Have a `~/.rpmmacros` file ready with the following content:

    %_signature gpg
    %_gpg_name Cyril Rohr # put the name of your key here

Pass the `--sign` option to `rpm-s3`:

    AWS_ACCESS_KEY="key" AWS_SECRET_KEY="secret" ./rpm-s3 --sign my-app-1.0.0.x86_64.rpm

In case if private key is password protected, you need to have gpg agent preconfigured with password.

Example

Ensure you have long cache ttl and option allow-preset-passphrase set in your ~/.gnupg/gpg-agent.conf,
or create one, if absent:

```sh
cat <<EOF >~/.gnupg/gpg-agent.conf
default-cache-ttl 46000
allow-preset-passphrase
EOF
```

If you introduced changes, reload agent

```sh
gpg-connect-agent RELOADAGENT /bye
```

If you get error message `gpg-connect-agent: can't connect to the agent: IPC connect call failed` , most likely
you will need to use more dirty way (usually centos):
```
pkill -9 gpg-agent
source <(gpg-agent --daemon)
```

Once you introduced changes, preset password for the key (point attention, that I am selecting grp portion of the key)

Mentioned `gpg-preset-passphrase` might be present in `/usr/libexec/gpg-preset-passphrase` or `/usr/lib/gnupg2/gpg-preset-passphrase` or other location, depending on your OS.


```
echo $SIGNING_PRIVATE_PASSPHRASE | /usr/lib/gnupg2/gpg-preset-passphrase -v -c $(gpg --list-secret-keys --with-fingerprint --with-colons | awk -F: '$1 == "grp" { print $10 }')
```

If you are doing that in cd/ci pipeline , I would recommend to isolate gpg keyring to only needed key - this makes 
part of locating grp a way easier


```sh
#!/bin/sh

export GNUPGHOME=/some/unique/directory/with/private/and/pubkey/files


cat $GNUPGHOME/public.key | gpg --import
rpm --import $GNUPGHOME/public.key
echo "SECRETPASSWORD" | gpg --batch --yes --passphrase-fd 0 --import $GNUPGHOME/private.key
```


If you still need to use pexpect, add -e / --expect parameter to sign using pexpect


### Import gpg key to install signed packages

    sudo rpm --import path/to/public/key # this also accepts URLs

## TODO

* Release as python package.
* Add spec and control files for RPM and DEB packaging.


## Side notes

One of the ideas was to get external repodata contents using native aws s3.

```py

from awscli.clidriver import create_clidriver
#aws_cli('s3', 'sync', 's3://my-bucket/master/repodata', 'zzz/master/repodata')
def aws_cli(*cmd):
    old_env = dict(os.environ)
    try:
        env = os.environ.copy()
        env['LC_CTYPE'] = u'en_US.UTF'
        os.environ.update(env)
        # Run awscli in the same process
        exit_code = create_clidriver().main(*cmd)
        if exit_code > 0:
            raise RuntimeError('AWS CLI exited with code {}'.format(exit_code))
    finally:
        os.environ.clear()
        os.environ.update(old_env)

```
