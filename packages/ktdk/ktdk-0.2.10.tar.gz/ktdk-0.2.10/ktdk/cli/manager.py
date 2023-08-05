import importlib
import importlib.machinery
import importlib.util
import logging
import shutil
import sys
from pathlib import Path

from ktdk import Config, KTDK

log = logging.getLogger(__name__)


class CliManager(object):
    def __init__(self, **kwargs):
        self._params = dict(**kwargs)
        self._ktdk = None

    @property
    def ktdk(self) -> KTDK:
        if self._ktdk is None:
            self._ktdk = self.get_ktdk()
        return self._ktdk

    @property
    def config(self) -> Config:
        return self.ktdk.config

    @property
    def workspace_dir(self) -> Path:
        return Path(self.ktdk.config['workspace']).absolute()

    @property
    def test_files_dir(self) -> Path:
        return Path(self.ktdk.config['test_files']).absolute()

    @property
    def submission_dir(self) -> Path:
        return Path(self.ktdk.config['submission']).absolute()

    @property
    def results_dir(self) -> Path:
        return Path(self.ktdk.config['results']).absolute()

    def load_project_files(self):
        module_path = self.test_files_dir / 'kontr_tests'
        sys.path.insert(0, str(module_path))
        path = module_path / self.config.get('entry_point')
        return _import_module_files('test_files', path)

    def get_ktdk(self, **kwargs):
        config = {**self._params, **kwargs}
        log.debug(f"[CFG] Config: {config}")
        ktdk = KTDK.get_instance(**config)
        return ktdk

    def load_suite(self):
        self.load_project_files()
        return self.ktdk

    def run_the_suite(self):
        ktdk = self.load_suite()
        if self.ktdk.config.devel and self.ktdk.config.clean:
            shutil.rmtree(self.ktdk.config.paths.workspace)
        ktdk.invoke()
        return ktdk


def _import_module_files(module_name: str, path: Path):
    full_path = str(path)
    loader = importlib.machinery.SourceFileLoader(module_name, full_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    log.info(f"[CLI] Loading module: {mod}")
    return mod
