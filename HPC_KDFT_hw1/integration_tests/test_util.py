from subprocess import Popen, PIPE
from tempfile import mkstemp
from zipfile import ZipFile
import logging
import os

from concrete.util import write_communication_to_buffer


DEFAULT_WAIT_TIMEOUT = 30
DEFAULT_WAIT_INTERVAL = 1


def run(args, decode=True, check=True, input_data=None):
    logging.info(' '.join(args))
    if decode and input_data is not None:
        input_data = input_data.encode('utf-8')
    p = Popen(args, stdout=PIPE, stderr=PIPE,
              stdin=PIPE if input_data is not None else None)
    (out_data, err_data) = p.communicate(input_data)
    if decode:
        out_data = out_data.decode('utf-8')
        err_data = err_data.decode('utf-8')
    if check:
        if p.returncode != 0:
            raise Exception(
                'process failed with return code {}: {}\nstderr:\n{}\n'.format(
                    p.returncode, ' '.join(args), err_data))
    return out_data


def force_remove_container(container_name):
    run(['docker', 'rm', '-f', container_name], check=False)


def force_remove_image(image_name):
    run(['docker', 'rmi', '-f', image_name], check=False)


def force_remove_volume(volume_name):
    run(['docker', 'volume', 'rm', '-f', volume_name], check=False)


def force_remove(path):
    os.remove(path)


def docker_build(dockerfile_path, image_name):
    force_remove_image(image_name)
    run(['docker', 'build', '-t', image_name, '-f', dockerfile_path, '.'])


def docker_run(image_name, *args, **kwargs):
    rm = kwargs.get('rm', False)
    d = kwargs.get('d', False)
    v = kwargs.get('v', None)
    network = kwargs.get('network', None)
    name = kwargs.get('name', None)
    if name is not None:
        force_remove_container(name)
    input_data = kwargs.get('input_data', None)
    if not set(kwargs).issubset([
            'rm', 'd', 'v', 'network', 'name', 'input_data']):
        raise ValueError('unrecognized kwargs: {}'.format(kwargs))
    if isinstance(v, tuple) or isinstance(v, list):
        v = ':'.join(v)
    if isinstance(network, tuple) or isinstance(network, list):
        network = ':'.join(network)
    return run(
        ['docker', 'run'] +
        (['--rm'] if rm else []) +
        (['-i'] if input_data is not None else []) +
        (['-d'] if d else []) +
        (['-v', v] if v else []) +
        (['--network', network] if network else []) +
        (['--name', name] if name else []) +
        [image_name] +
        list(args),
        input_data=input_data,
    )


def docker_volume_create(volume_name):
    force_remove_volume(volume_name)
    run(['docker', 'volume', 'create', '--name', volume_name])


def docker_rm(container_name, f=False):
    run(['docker', 'rm'] + (['-f'] if f else []) + [container_name])


def docker_cp(src_loc, dst_loc, L=True):
    if isinstance(src_loc, tuple) or isinstance(src_loc, list):
        src_loc = ':'.join(src_loc)
    if isinstance(dst_loc, tuple) or isinstance(dst_loc, list):
        dst_loc = ':'.join(dst_loc)
    run(['docker', 'cp'] + (['-L'] if L else []) + [src_loc, dst_loc])


def wait_concrete_service(container_name, service_name,
                          host='localhost', port=9090,
                          wait_timeout=DEFAULT_WAIT_TIMEOUT,
                          wait_interval=DEFAULT_WAIT_INTERVAL):
    docker_run(
        'concrete-python-image',
        'wait-concrete-service.py', service_name,
        '--host', host,
        '--port', str(port),
        '--timeout', str(wait_timeout),
        '--sleep-interval', str(wait_interval),
        rm=True, network=('container', container_name))


def mktemp_path(suffix):
    (fd, path) = mkstemp(suffix=suffix)
    os.close(fd)
    return path


class CommunicationWriterZip(object):
    def __init__(self, path):
        self.path = path
        self.zip_f = None

    def open(self):
        self.zip_f = ZipFile(self.path, 'w')

    def close(self):
        self.zip_f.close()

    def write(self, comm):
        self.zip_f.writestr(comm.id + '.concrete',
                            write_communication_to_buffer(comm))

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def print_assert(expected_text, actual_text, predicate, message):
    '''
    If predicate evaluates to False, print expected_text, actual_text,
    and message to stderr and abort.
    '''
    assert predicate, '''\n
expected index:
{expected_text}
actual index:
{actual_text}
error: {message}
'''.format(expected_text=expected_text, actual_text=actual_text,
           message=message)


def read_index(lines, actual, expected_text, actual_text):
    '''
    Read index from list of text lines, running tests (passing
    expected_text and actual_text to print_assert) if actual
    evaluates to True, and return a dictionary containing the
    list of communication IDs in the first line of the index and a
    dictionary mapping each word to a dictionary representing the
    corresponding line of the index.  Each word's dictionary contains
    the IDF and a list of (communication ID, TF) pairs.
    '''
    comm_ids = lines[0].strip().split('\t')
    word_dicts = dict()
    for line in lines[1:]:
        pieces = line.strip().split('\t')
        word = pieces[0]
        idf = float(pieces[1])
        comm_id_tf_pairs = []
        comm_positions = []
        for comm_id_tf_pair_str in pieces[2:]:
            colon_pos = comm_id_tf_pair_str.rindex(':')
            comm_pos = int(comm_id_tf_pair_str[:colon_pos])
            comm_id = comm_ids[comm_pos]
            comm_positions.append(comm_pos)
            tf = int(float(comm_id_tf_pair_str[colon_pos + 1:]))
            if actual:
                print_assert(
                    expected_text, actual_text,
                    comm_id not in set(c for (c, _) in comm_id_tf_pairs),
                    'word {} references comm {} twice'.format(word, comm_id))
            comm_id_tf_pairs.append((comm_id, tf))
        if actual:
            print_assert(
                expected_text, actual_text,
                word not in word_dicts,
                'index contains word {} twice'.format(word))
        if actual:
            print_assert(
                expected_text, actual_text,
                comm_positions == sorted(comm_positions),
                'comm references for word {} are not sorted'.format(word))
        word_dicts[word] = dict(idf=idf, comm_id_tf_pairs=comm_id_tf_pairs)
    return dict(comm_ids=comm_ids, word_dicts=word_dicts)


def near(x, y, atol=1e-4, rtol=1e-3):
    '''
    Return true if float x is near float y.
    '''
    return abs(x - y) <= atol + rtol * abs(y)


def assert_index_near(expected_text, actual_text):
    expected_lines = expected_text.rstrip('\n').split('\n')
    expected_index = read_index(expected_lines, False, expected_text, '')
    actual_lines = actual_text.rstrip('\n').split('\n')
    actual_index = read_index(actual_lines, True, '', actual_text)

    print_assert(
        expected_text, actual_text,
        set(expected_index['comm_ids']) == set(actual_index['comm_ids']),
        'actual index and expected index do not have same comm ids')

    print_assert(
        expected_text, actual_text,
        len(expected_index['word_dicts']) == len(actual_index['word_dicts']),
        'actual index and expected index do not have same number of words')

    actual_comm_ids = actual_index['comm_ids']
    print_assert(
        expected_text, actual_text,
        set(expected_index['comm_ids']) == set(actual_comm_ids),
        'actual index and expected index do not have same comm ids')

    for (word, expected_word_dict) in expected_index['word_dicts'].items():
        print_assert(
            expected_text, actual_text,
            word in actual_index['word_dicts'],
            'actual index does not contain expected word {}'.format(word))
        actual_word_dict = actual_index['word_dicts'][word]
        print_assert(
            expected_text, actual_text,
            near(expected_word_dict['idf'], actual_word_dict['idf']),
            'actual IDF {} for word {} does not match expected {}'.format(
                actual_word_dict['idf'], word, expected_word_dict['idf']))
        for (expected_comm_id,
                expected_tf) in expected_word_dict['comm_id_tf_pairs']:
            print_assert(
                expected_text, actual_text,
                [1 for (comm_id, tf) in actual_word_dict['comm_id_tf_pairs']
                    if expected_comm_id == comm_id and expected_tf == tf],
                'no communication, tf pair matching {}, {} for word {}'.format(
                    expected_comm_id, expected_tf, word))


def text_to_lines(text):
    lines = []
    start = 0
    while start < len(text):
        end = text.find('\n', start)
        lines.append(text[start:end])
        start = end + 1

    return lines
