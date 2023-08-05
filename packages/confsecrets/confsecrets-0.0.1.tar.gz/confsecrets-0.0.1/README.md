# confsecrets
[![Build Status](https://travis-ci.org/danizen/confsecrets.svg?branch=master)](https://travis-ci.org/danizen/confsecrets) [![Coverage Status](https://coveralls.io/repos/github/danizen/confsecrets/badge.svg?branch=master)](https://coveralls.io/github/danizen/confsecrets?branch=master)

Simple utility/package to symmetrically encrypt/decrypt application secrets.

## Description

It is often difficult for developers to secure passwords for databases, search
engines, directory services, etc.  Security wishes to make sure these secrets
are centralized, but this adds a dependency on an external service, not to
mention code complexity.

Several solutions exist, but these are often silos without any abstraction built
around them.

The goal of this project is to provide APIs that wrap the simplest solutions that
are actually solutions, namely:
 - Keeping passwords as encrypted values on the filesystem, with a passphrase in the code.

Future versions will add the ability to keep the encrypted material in S3, or
another cloud storage provider, and to keep the passphrase from which a key is
derived also in cloud storage.

## Other Tools

### pyjks

- Doesn't support saving jceks
- Can load from string, so we could use it as keystore format and add S3 and stuff

### keyczar

- Manages encryption, but doesn't support MFA keys - e.g. not a vault in which to store
  encrypted material.
- Doesn't directly support use of S3 or HashiCorp vault as a backend, only itself.
- Doesn't offer management of secrets, just management of keys.

### EC2 Secrets Manager

- Again, this is a central play, and locks you in somewhat to the vendor.

## Concept of Operation

The goal here is to reach the point where we can keep multiple secrets in the same 
encrypted wodge, decrypted with the same passwords, and provide some command-line over 
them that is easily integrated into Django.  We want to act locally but think globally.

How about this:
  - implement `confsecrets\vault.py` which contains a `Vault` class that is a subclass of UserDict, maybe OrderedDict.
  - The vault has the following init:

          Vault(key=, salt=, path=, encoder=, decoder=)

  - It implements it encrypts using the the salt and key to base64.
  - Encrypting immediately flushes the file that has been loaded
  - On decrypt, it checks to see if the file has changed, and reloads the underlying data in that case.
  - On decrypt, it reverses the process.

There is a concept of a "default vault" whose configuration is controlled by environment variables or through the API.
The "default vault" is is a singleton.   

Django integration is provided via a `confsecrets.django` application that allows the configuration to be provided by settings:

    CONFSECRETS_SALT = b'89982hto'
    CONFSECRETS_KEY = 'This is not an example'
    CONFSECRETS_VAULT = os.path.join(BASE_DIR, 'vault.yaml')

This initializes the default vault during configuration freeze. Otherwise, the default vault's configuration is controlled by the environment variables.

This is secure as long as the vault file are not stored in git, and then it becomes obfuscation. It is best when both the passphrase from which a key is derived is also outside of git.

Saving secrets becomes easy through a management command to populate the vault:

  * `listsecrets` - lists the secrets stored in the vault, along with their value
  * `putsecret <name> [--value <value>]` - uses value if present, otherwise uses stdin
  * `getsecret <name>` - typical options, outputs the secret to the stdout
  * `rmsecret <name>` - removes an encrypted value from the vault

With the system configured, dealing with the vault becomes as easy as using Secret objects:

    ELASTICSEARCH_PASSWORD = Secret('name')

To access it, you can treat it like a string:

    from django.conf import settings

    settings.ES_PASSWORD.decrypt()

The secret also acts like a string:

    int(str(settings.ES_PASSWORD))

or:

    auth_string = "%s:%s" % (username, settings.ES_PASSWORD)
  
This will fail for a number of reasons with clear exceptions:
   - If  the configuration is not available via settings or environment variables
   - If the vault is not-present
   - If the vault doesn't have that key in it

Vault would then know how to deal with the operations described above.

## Self-critique

This way of doing things does not fully comply the [Twelve-Factor App](https://12factor.net/) way of managing the environment.  Django's settings are similarly response to the environment while recognizing that configuration solely via the environment is complicated.

## Roadmap

Not sure on the priority of these:

- Add support for placing the vault on S3.  Vault becomes polymorphic because if path is an URL, then we will create a different sub-class of `Vault` using an override of `__new__`.  A local path vault is still standard.

- Separate cli from Django management commands.

- Add support for placing the passphrase on S3 similarly.

- Support secret versioning, so that it is possible for a developer to push a new value for a password from the desktop,
  and then change the password to some backend.

- Add support for a default value for a secret, so that you get the default instead of KeyError

- Add support/integration for Flask - it can surely be used without this because pbe, secret, and vault sub-modules are independent.

- Move to cryptodome once that package is out of Beta.

## Status

Have implemented the `Vault`, `DefaultVault`, and initial `Secret` facilities.  Django management commands and integration needs tests.
