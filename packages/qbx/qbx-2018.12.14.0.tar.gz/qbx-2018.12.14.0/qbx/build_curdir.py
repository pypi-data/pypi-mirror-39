import arrow
import redis

from .cdi import docker_retag_and_push, get_docker_client

redis_client = redis.StrictRedis('redis.svc.qbtrade.org')
doc = """
Usage:
    build-curdir [options]
    
Options:
    --repo=<repo>
    --no-cache
"""


def build_curdir(argv):
    import os
    from docopt import docopt as docoptinit
    import json
    import sys
    docopt = docoptinit(doc, argv)
    folder = os.path.abspath('.')

    # parent_hash = get_hash_of_dirs(folder)
    # if not docopt['--always-rebuild']:
    #     if folder in db and db[folder] == parent_hash:
    #         print('{} hash check sum'.format(folder))
    #         return
    success = False
    if docopt['--repo']:
        repo = docopt['--repo']
    else:
        repo = os.path.basename(folder)
    tag = 'qbtrade/{}:latest'.format(repo)
    print('------build------', folder, tag)
    for line in get_docker_client().build(path=folder,
                                          dockerfile='Dockerfile',
                                          nocache=docopt['--no-cache'],
                                          tag=tag,
                                          rm=True):
        try:
            line = line.decode('utf8')
            print(json.loads(line)['stream'], end='')
        except:
            print(line, end='')
        if 'Successfully built' in line:
            success = True
    if not success:
        sys.exit(1)
    print('------push------')
    # cfg = load_cdi_config(folder)
    # if cfg.get('public', True):
    #     docker_push(tag)
    #     docker_retag_and_push(tag, tag + '-' + date_str)
    # else:
    #     print('only push to private repo')
    if os.environ.get('QB_REGION') == 'alihk':
        docker_retag_and_push_all(tag, 'registry-vpc.cn-hongkong.aliyuncs.com/' + tag)
    else:
        docker_retag_and_push_all(tag, 'registry.cn-hongkong.aliyuncs.com/' + tag)


def docker_retag_and_push_all(tag, param):
    # push all qbtrade/ot-rpc:latest registry-vpc.cn-hongkong.aliyuncs.com/qbtrade/ot-rpc:latest
    print('push all', tag, param)
    repo = tag.split('/')[-1].split(':')[0]
    date_str = arrow.now().strftime('%Y%m%d')
    datetime_str = arrow.now().strftime('%Y%m%d-%H%M')
    print(repo, datetime_str)
    redis_client.lpush('cache:docker-image:' + repo, datetime_str)
    docker_retag_and_push(tag, param)
    if param.endswith(':latest'):
        docker_retag_and_push(tag, param.replace('latest', '') + date_str)
        docker_retag_and_push(tag, param.replace('latest', '') + datetime_str)
    else:
        docker_retag_and_push(tag, param + '-' + date_str)
        docker_retag_and_push(tag, param + '-' + datetime_str)

    # docker_retag_and_push_all(tag, 'registry.cn-hangzhou.aliyuncs.com/' + tag)

    # db[folder] = parent_hash
