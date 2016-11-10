"""
Role tests
"""
import pytest

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images(
    'infopen/ubuntu-trusty-ssh:0.1.0',
    'infopen/ubuntu-xenial-ssh-py27:0.2.0'
)


def test_packages(SystemInfo, Package):

    if SystemInfo.codename == 'trusty':
        assert Package('php5-fpm').is_installed

    elif SystemInfo.codename == 'xenial':
        assert Package('php-fpm').is_installed


@pytest.mark.parametrize('instance_name', [('fpm'), ('fpm-foo')])
def test_main_config_file(SystemInfo, File, instance_name):

    cfg_files_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_file_path = '/etc/php5/%s/php-fpm.conf' % instance_name
    elif SystemInfo.codename == 'xenial':
        cfg_file_path = '/etc/php/7.0/%s/php-fpm.conf' % instance_name

    cfg_file = File(cfg_file_path)

    assert cfg_file.exists
    assert cfg_file.is_file
    assert cfg_file.contains('[global]')


@pytest.mark.parametrize('instance_name', [('fpm'), ('fpm-foo')])
def test_fpm_php_ini_config_file(SystemInfo, File, instance_name):

    cfg_file_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_file_path = '/etc/php5/%s/php.ini' % instance_name
    elif SystemInfo.codename == 'xenial':
        cfg_file_path = '/etc/php/7.0/%s/php.ini' % instance_name

    cfg_file = File(cfg_file_path)

    assert cfg_file.exists
    assert cfg_file.is_file
    assert cfg_file.contains('[PHP]')


@pytest.mark.parametrize('instance_name', [('fpm'), ('fpm-foo')])
def test_unmanaged_pool_config_file(SystemInfo, File, instance_name):

    cfg_pool_dir_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_pool_dir_path = '/etc/php5/%s/pool.d/' % instance_name
    elif SystemInfo.codename == 'xenial':
        cfg_pool_dir_path = '/etc/php/7.0/%s/pool.d/' % instance_name

    pool_file = File(cfg_pool_dir_path + 'www.conf')

    assert pool_file.exists is False


@pytest.mark.parametrize('instance_name', [('fpm'), ('fpm-foo')])
def test_managed_pool_config_file(SystemInfo, File, instance_name):

    cfg_pool_dir_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_pool_dir_path = '/etc/php5/%s/pool.d/' % instance_name
    elif SystemInfo.codename == 'xenial':
        cfg_pool_dir_path = '/etc/php/7.0/%s/pool.d/' % instance_name

    pool_file = File(cfg_pool_dir_path + 'foobar.conf')

    assert pool_file.exists
    assert pool_file.is_file
    assert pool_file.contains('[foobar]')


@pytest.mark.parametrize('instance_name,service_name', [
    ('fpm', 'default'),
    ('fpm-foo', 'fpm-foo')
])
def test_init_files(SystemInfo, File, instance_name, service_name):

    default_service_name = ''

    if SystemInfo.codename == 'trusty':
        default_service_name = 'php5-fpm'
    elif SystemInfo.codename == 'xenial':
        default_service_name = 'php7.0-fpm'

    if service_name == 'default':
        init_file = File('/etc/init.d/%s' % default_service_name)
    else:
        init_file = File('/etc/init.d/%s' % service_name)

    assert init_file.exists
    assert init_file.is_file
    assert init_file.contains('for %s instance' % instance_name)


@pytest.mark.parametrize('instance_name,service_name', [
    ('fpm', 'default'),
    ('fpm-foo', 'fpm-foo')
])
def test_servicess(SystemInfo, Service, instance_name, service_name):

    default_service_name = ''

    if SystemInfo.codename == 'trusty':
        default_service_name = 'php5-fpm'
    elif SystemInfo.codename == 'xenial':
        default_service_name = 'php7.0-fpm'

    if service_name == 'default':
        service = Service(default_service_name)
    else:
        service = Service(service_name)

    assert service.is_running
    assert service.is_enabled
