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


def test_main_config_file(SystemInfo, File):

    cfg_file_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_file_path = '/etc/php5/fpm/php-fpm.conf'
    elif SystemInfo.codename == 'xenial':
        cfg_file_path = '/etc/php/7.0/fpm/php-fpm.conf'

    cfg_file = File(cfg_file_path)

    assert cfg_file.exists
    assert cfg_file.is_file
    assert cfg_file.contains('[global]')


def test_fpm_php_ini_config_file(SystemInfo, File):

    cfg_file_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_file_path = '/etc/php5/fpm/php.ini'
    elif SystemInfo.codename == 'xenial':
        cfg_file_path = '/etc/php/7.0/fpm/php.ini'

    cfg_file = File(cfg_file_path)

    assert cfg_file.exists
    assert cfg_file.is_file
    assert cfg_file.contains('[PHP]')


def test_unmanaged_pool_config_file(SystemInfo, File):

    cfg_pool_dir_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_pool_dir_path = '/etc/php5/fpm/pool.d/'
    elif SystemInfo.codename == 'xenial':
        cfg_pool_dir_path = '/etc/php/7.0/fpm/pool.d/'

    pool_file = File(cfg_pool_dir_path + 'www.conf')

    assert pool_file.exists is False


def test_managed_pool_config_file(SystemInfo, File):

    cfg_pool_dir_path = ''

    if SystemInfo.codename == 'trusty':
        cfg_pool_dir_path = '/etc/php5/fpm/pool.d/'
    elif SystemInfo.codename == 'xenial':
        cfg_pool_dir_path = '/etc/php/7.0/fpm/pool.d/'

    pool_file = File(cfg_pool_dir_path + 'foobar.conf')

    assert pool_file.exists
    assert pool_file.is_file
    assert pool_file.contains('[foobar]')
