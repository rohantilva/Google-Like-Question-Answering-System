from pytest import fixture
from concrete.util import create_comm
import re

from test_util import (
    mktemp_path, CommunicationWriterZip, wait_concrete_service,
    assert_index_near,
    force_remove, force_remove_container, force_remove_volume,
    force_remove_image,
    docker_run, docker_build, docker_cp, docker_volume_create,
)


STOP_WORD_RE = re.compile('^s\d+$')


def make_stop_word_text(num_words=250):
    text = ''
    for word_num in range(num_words):
        text += ' s{}'.format(word_num)
        if (word_num + 1) % 10 == 0:
            text += '\n'
        if (word_num + 1) % 50 == 0:
            text += '\n'

    return text


@fixture(scope='module')
def index_volume():
    docker_build('Dockerfile.concrete_python', 'concrete-python-image')
    docker_build('Dockerfile.index', 'indexing-image')

    docker_volume_create('data')
    docker_volume_create('index')

    zip_path = mktemp_path('.zip')
    with CommunicationWriterZip(zip_path) as writer:
        writer.write(create_comm(
            'test comm 0',
            'w1\n{}\nw1\n\nw2 w4\n'.format(make_stop_word_text())))
        writer.write(create_comm(
            'test comm 1',
            '{}'.format(make_stop_word_text())))
        writer.write(create_comm(
            'test comm 2',
            '{}\nw3\nw3 w2\n'.format(make_stop_word_text())))

    docker_run(
        'concrete-python-image', 'sleep', 'infinity',
        d=True, v=('data', '/mnt/data'), name='data-copy')
    docker_cp(zip_path, ('data-copy', '/mnt/data/comms.tar.gz'))
    force_remove_container('data-copy')

    docker_run(
        'concrete-python-image',
        'fetch-server.py', '/mnt/data/comms.tar.gz',
        '--host', 'localhost', '--port', '9090',
        d=True, v=('data', '/mnt/data'), name='fetch')
    wait_concrete_service('fetch', 'FetchCommunication')
    docker_run(
        'indexing-image',
        network=('container', 'fetch'), rm=True,
        v=('index', '/mnt/index'))

    yield 'index'

    force_remove_container('data-copy')
    force_remove_container('fetch')
    force_remove_volume('data')
    force_remove_volume('index')
    force_remove(zip_path)
    force_remove_image('indexing-image')
    force_remove_image('concrete-python-image')


def test_top_terms(index_volume):
    top_terms_text = docker_run(
        'concrete-python-image', 'cat', '/mnt/index/top-terms.txt',
        rm=True, v=(index_volume, '/mnt/index'))
    top_terms = top_terms_text.rstrip('\n').split('\n')
    assert len(top_terms) == 50
    assert len([t for t in top_terms if STOP_WORD_RE.match(t)]) == 50
    assert len(set(top_terms)) == 50


def test_index(index_volume):
    actual_text = docker_run(
        'concrete-python-image', 'gunzip', '-c',
        '/mnt/index/index.gz',
        rm=True, v=(index_volume, '/mnt/index'))
    expected_text = '''\
test comm 0	test comm 1	test comm 2
w1	1.098612	0:2
w2	0.405465	0:1	2:1
w3	1.098612	2:2
w4	1.098612	0:1
'''
    assert_index_near(expected_text, actual_text)
