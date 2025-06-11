"""The Commander for the Observatory Environment system."""

from __future__ import annotations

import os
import subprocess as sp
from typing import Any

from structlog.stdlib import BoundLogger

from ..domain.models import PackageUpdate, UserInfo
from .commander import Commander

__all__ = ["ObsEnvCommander"]


class ObsEnvCommander(Commander):
    """Handle calls to the obsenv storage."""

    def __init__(self, *, logger: BoundLogger) -> None:
        super().__init__(logger=logger)

    def __decode_output(self, output: sp.CompletedProcess[bytes]) -> str:
        decoded_output = output.stdout.decode("utf-8")
        return decoded_output[:-1]

    def __add_user_info_to_env(self, user_info: UserInfo) -> dict[str, Any]:
        new_env = os.environ.copy()
        new_env["SUDO_USER"] = user_info.uname
        new_env["SUDO_UID"] = user_info.uid
        return new_env

    def get_all_package_versions(self, user_info: UserInfo) -> tuple[str, str]:
        updated_env = self.__add_user_info_to_env(user_info)
        self._logger.debug(f"Environment: {updated_env}")
        cmd1 = ["manage_obs_env", "--action", "show-original-versions"]
        cmd2 = ["manage_obs_env", "--action", "show-current-versions"]

        ov = sp.run(
            cmd1,
            stdout=sp.PIPE,
            stderr=sp.STDOUT,
            check=False,
            env=updated_env,
        )
        decoded_ov = self.__decode_output(ov)
        self._logger.debug(decoded_ov)
        cv = sp.run(
            cmd2,
            stdout=sp.PIPE,
            stderr=sp.STDOUT,
            check=False,
            env=updated_env,
        )
        decoded_cv = self.__decode_output(cv)
        self._logger.debug(decoded_cv)

        return decoded_ov, decoded_cv

    def update_package_version(self, info: PackageUpdate) -> str:
        action = "checkout-version" if info.is_tag else "checkout-branch"
        cmd = [
            "manage_obs_env",
            "--action",
            action,
            "--repository",
            info.name.lower(),
            "--branch-name",
            info.version,
        ]
        updated_env = self.__add_user_info_to_env(
            UserInfo(uname=info.username, uid=info.userid)
        )
        output = sp.run(
            cmd, stdout=sp.PIPE, stderr=sp.STDOUT, check=False, env=updated_env
        )
        self._logger.debug(str(output))
        return self.__decode_output(output)
