import docker
import docker.errors
from loguru import logger

from src.config import Settings


class DockerInit:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DockerInit, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.docker = docker.from_env()
        self.image = None
        self.container = None

    def _build_image(self, dfile_path: str, image_tag: str = "db_test") -> None:
        self.docker.images.build(path=dfile_path, tag=image_tag, rm=True)
        self.image: str = image_tag

    def _create_container(
        self,
        cname: str,
        ports: dict[str:int],
        cmd: str | list = ["-dA" "-rm"],
    ) -> None:
        try:
            self.docker.containers.run(
                image=self.image,
                name=cname,
                command=cmd,
                ports=ports,
                remove=True,
                detach=True,
            )
        except docker.errors.APIError:
            pass
        self.container: str = cname

    def run(self, dockerfile_path: str, ports: dict[str:int]) -> None:
        path: str = dockerfile_path
        self._build_image(path, "db_test_image")
        self._create_container(cname="db_test", ports=ports)


def run_docker(path: str, port: str) -> None:
    s: Settings = Settings.get_settings()
    if s.docker.DOCKER_MODE:
        logger.debug("Docker mode enabled. Starting...")
        result_port: dict = {5432: port + "/tcp"}
        d: DockerInit = DockerInit()
        d.run(dockerfile_path=path, ports=result_port)
        logger.debug("Docker container is running now")
    else:
        logger.debug("Docker mode disabled.")
