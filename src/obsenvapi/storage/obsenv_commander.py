"""The Commander for the Observatory Environment system."""

from __future__ import annotations

import subprocess as sp

from structlog.stdlib import BoundLogger

from .commander import Commander

__all__ = ["ObsEnvCommander"]


class ObsEnvCommander(Commander):
    """Handle calls to the obsenv storage."""

    def __init__(self, *, logger: BoundLogger) -> None:
        super().__init__(logger=logger)

    def __decode_output(self, output: sp.CompletedProcess[bytes]) -> str:
        decoded_output = output.stdout.decode("utf-8")
        return decoded_output[:-1]

    def get_all_package_versions(self) -> tuple[str, str]:
        cmd1 = ["manage_obs_env", "--action", "show-original-versions"]
        cmd2 = ["manage_obs_env", "--action", "show-current-versions"]

        ov = sp.run(cmd1, stdout=sp.PIPE, stderr=sp.STDOUT, check=False)
        decoded_ov = self.__decode_output(ov)
        self._logger.debug(decoded_ov)
        cv = sp.run(cmd2, stdout=sp.PIPE, stderr=sp.STDOUT, check=False)
        decoded_cv = self.__decode_output(cv)
        self._logger.debug(decoded_cv)

        return decoded_ov, decoded_cv
