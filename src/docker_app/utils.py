import docker
import docker.errors
from src.config import Settings
from loguru import logger

class DockerInit:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DockerInit, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.docker = docker.from_env()
        self.image = None
        self.container = None

    def _build_image(self, dfile_path: str,
                     image_tag: str = 'db_test'
                     ) -> None:
        self.docker.images.build(path=dfile_path,
                                 tag=image_tag,
                                 rm=True
                                 )
        self.image = image_tag

    def _create_container(self, cname: str,
                          cmd: str | list = ['-dA' '-rm']
                          ) -> None:
        try:
            self.docker.containers.run(image=self.image,
                                       name=cname,
                                       command=cmd,
                                       remove=True,
                                       detach=True,
                                       )
        except docker.errors.APIError:
            pass
        self.container = cname

    def run(self, dockerfile_path: str) -> None:
        path = dockerfile_path
        self._build_image(path, 'db_test_image')
        self._create_container(cname='db_test')


def run_docker(path: str) -> None:
    s = Settings.get_settings()
    if s.docker.DOCKER_MODE:
        logger.debug('Docker mode enabled. Starting...')
        d = DockerInit()
        d.run(path)
        logger.debug('Docker container is running now')
    else:
        logger.debug('Docker mode disabled.')
