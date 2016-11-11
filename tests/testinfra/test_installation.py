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


@pytest.mark.parametrize('instance_name,pool_name', [
    ('fpm', 'foobar'),
    ('fpm-foo', 'foobar2')
])
def test_managed_pool_config_file(SystemInfo, File, instance_name, pool_name):

    cfg_pool_dir_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_pool_dir_path = '/etc/php5/%s/pool.d' % instance_name
    elif SystemInfo.codename == 'xenial':
        cfg_pool_dir_path = '/etc/php/7.0/%s/pool.d' % instance_name

    pool_file = File('%s/%s.conf' % (cfg_pool_dir_path, pool_name))

    assert pool_file.exists
    assert pool_file.is_file
    assert pool_file.contains('[%s]' % pool_name)


@pytest.mark.parametrize('instance_name,service_name', [
    ('fpm', 'default'),
    ('fpm-foo', 'fpm-foo')
])
def test_init_files(SystemInfo, File, instance_name, service_name):

    real_service_name = ''

    if service_name == 'default':
        if SystemInfo.codename == 'trusty':
            real_service_name = 'php5-fpm'
        elif SystemInfo.codename == 'xenial':
            real_service_name = 'php7.0-fpm'
    else:
        real_service_name = service_name

    init_file = File('/etc/init.d/%s' % real_service_name)

    assert init_file.exists
    assert init_file.is_file
    assert init_file.contains('for %s instance' % instance_name)


@pytest.mark.parametrize('instance_name,service_name', [
    ('fpm', 'default'),
    ('fpm-foo', 'fpm-foo')
])
def test_services(SystemInfo, Service, instance_name, service_name):

    real_service_name = ''

    if service_name == 'default':
        if SystemInfo.codename == 'trusty':
            real_service_name = 'php5-fpm'
        elif SystemInfo.codename == 'xenial':
            real_service_name = 'php7.0-fpm'
    else:
        real_service_name = service_name

    service = Service(real_service_name)

    assert service.is_enabled
    assert service.is_running
