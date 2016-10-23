# php-fpm

[![Build Status](https://travis-ci.org/infOpen/ansible-role-php-fpm.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-php-fpm)

Install php-fpm package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role has some testing methods.

To use locally testing methods, you need to install Docker and/or Vagrant and Python requirements:

* Create and activate a virtualenv
* Install requirements

```
pip install -r requirements_dev.txt
```

### Automatically with Travis

Tests runs automatically on Travis on push, release, pr, ... using docker testing containers

### Locally with Docker

You can use Docker to run tests on ephemeral containers.

```
make test-docker
```

### Locally with Vagrant

You can use Vagrant to run tests on virtual machines.

```
make test-vagrant
```

## Role Variables

### Default role variables

``` yaml
```

### Define custom settings for php.ini or php-fpm.conf files

You can define custom settings for php.ini or php-fpm.conf using:
* php.ini: 'php_fpm_config_php_ini'
* php-fpm.conf: 'php_fpm_config_main'

``` yaml
php_fpm_config_main:
  - section: 'global'
    option: 'my_option'
    value: 'my_value'
    state: 'present'
```

## Dependencies

None

## Example Playbook

    - hosts: servers
      roles:
         - { role: infOpen.php-fpm }

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro

