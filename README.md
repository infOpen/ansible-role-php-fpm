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
# Defaults vars file for php-fpm role

php_fpm_apt_update_cache: True
php_fpm_apt_cache_valid_time: 3600
php_fpm_packages: "{{ _php_fpm_packages }}"
php_fpm_packages_state: 'present'

php_fpm_binary_name: "{{ _php_fpm_binary_name }}"
php_fpm_service_name: "{{ _php_fpm_service_name }}"

php_fpm_config_base: "{{ _php_fpm_config_base }}"
php_fpm_config_owner: 'root'
php_fpm_config_group: 'root'
php_fpm_config_files_mode: '0644'

php_fpm_pid_file: "{{ _php_fpm_pid_file }}"
php_fpm_error_log_file: "{{ _php_fpm_error_log_file }}"

# php-fpm.conf configuration file configuration
php_fpm_config_main:
  - section: 'global'
    option: 'pid'
    value: "{{ php_fpm_pid_file }}"
  - section: 'global'
    option: 'error_log'
    value: "{{ php_fpm_error_log_file }}"
  - section: 'global'
    option: 'include'
    value: "{{ php_fpm_config_base }}/pool.d/*.conf"

# php.ini configuration file configuration
php_fpm_config_php_ini: []

# Pools default settings
php_fpm_pool_defaults:
  pm: dynamic
  pm.max_children: 5
  pm.start_servers: 2
  pm.min_spare_servers: 1
  pm.max_spare_servers: 3
  pm.status_path: /status

php_fpm_pools: []
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

### Define pools configuration

```yaml
php_fpm_pools:
  - name: 'foobar'
    user: 'www-data'
    group: 'www-data'
    listen: '/var/run/php5-fpm-foobar.sock'
    listen.owner: 'www-data'
    listen.group: 'www-data'
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

