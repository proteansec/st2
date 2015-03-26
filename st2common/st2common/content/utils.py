# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pipes

from oslo.config import cfg

from st2common.constants.action import LIBS_DIR as ACTION_LIBS_DIR
from st2common.util.types import OrderedSet

__all__ = [
    'get_system_packs_base_path',
    'get_packs_base_paths',
    'get_pack_base_path',
    'get_pack_directory',
    'check_pack_directory_exists',
    'check_pack_content_directory_exists'
]


def get_system_packs_base_path():
    """
    Return a path to the directory where system packs are stored.

    :rtype: ``str``
    """
    return cfg.CONF.content.system_packs_base_path


def get_packs_base_paths():
    """
    Return a list of base paths which are searched for integration packs.

    :rtype: ``list``
    """
    system_packs_base_path = get_system_packs_base_path()
    packs_base_paths = cfg.CONF.content.packs_base_paths or ''

    # Remove trailing colon (if present)
    if packs_base_paths.endswith(':'):
        packs_base_paths = packs_base_paths[:-1]

    result = []
    # System path is always first
    if system_packs_base_path:
        result.append(system_packs_base_path)

    packs_base_paths = packs_base_paths.split(':')

    result = result + packs_base_paths
    result = [path for path in result if path]
    result = list(OrderedSet(result))
    return result


def check_pack_directory_exists(pack):
    """
    Check if a provided pack exists in one of the pack paths.

    :param pack: Pack name.
    :type pack: ``str``

    :rtype: ``bool``
    """
    packs_base_paths = get_packs_base_paths()

    for base_dir in packs_base_paths:
        pack_path = os.path.join(base_dir, pack)
        if os.path.exists(pack_path):
            return True

    return False


def check_pack_content_directory_exists(pack, content_type):
    """
    Check if a provided pack exists in one of the pack paths.

    :param pack: Pack name.
    :type pack: ``str``

    :param content_type: Content type (actions, sensors, rules).
    :type content_type: ``str``

    :rtype: ``bool``
    """
    packs_base_paths = get_packs_base_paths()

    for base_dir in packs_base_paths:
        pack_content_pack = os.path.join(base_dir, pack, content_type)
        if os.path.exists(pack_content_pack):
            return True

    return False


def get_pack_base_path(pack_name):
    """
    Return full absolute base path to the content pack directory.

    Note: This function looks for a pack in all the load paths and return path to the first pack
    which matched the provided name.

    If a pack is not found, we return a pack which points to the first packs directory (this is
    here for backward compatibility reasons).

    :param pack_name: Content pack name.
    :type pack_name: ``str``

    :rtype: ``str``
    """
    if not pack_name:
        return None

    packs_base_paths = get_packs_base_paths()
    for packs_base_path in packs_base_paths:
        pack_base_path = os.path.join(packs_base_path, pipes.quote(pack_name))
        pack_base_path = os.path.abspath(pack_base_path)

        if os.path.isdir(pack_base_path):
            return pack_base_path

    # Path with the provided name not found
    pack_base_path = os.path.join(packs_base_paths[0], pipes.quote(pack_name))
    pack_base_path = os.path.abspath(pack_base_path)
    return pack_base_path


def get_pack_directory(pack_name):
    """
    Retrieve a directory for the provided pack.

    If a directory for the provided pack doesn't exist in any of the search paths, None
    is returned instead.

    Note: If same pack exists in multiple search path, path to the first one is returned.

    :param pack_name: Pack name.
    :type pack_name: ``str``

    :return: Pack to the pack directory.
    :rtype: ``str`` or ``None``
    """
    packs_base_paths = get_packs_base_paths()
    for packs_base_path in packs_base_paths:
        pack_base_path = os.path.join(packs_base_path, pipes.quote(pack_name))
        pack_base_path = os.path.abspath(pack_base_path)

        if os.path.isdir(pack_base_path):
            return pack_base_path

    return None


def get_entry_point_abs_path(pack=None, entry_point=None):
    """
    Return full absolute path of an action entry point in a pack.

    :param pack_name: Content pack name.
    :type pack_name: ``str``
    :param entry_point: Action entry point.
    :type entry_point: ``str``

    :rtype: ``str``
    """
    if entry_point is not None and len(entry_point) > 0:
        if os.path.isabs(entry_point):
            return entry_point

        pack_base_path = get_pack_base_path(pack_name=pack)
        entry_point_abs_path = os.path.join(pack_base_path, 'actions', pipes.quote(entry_point))
        return entry_point_abs_path
    else:
        return None


def get_action_libs_abs_path(pack=None, entry_point=None):
    """
    Return full absolute path of libs for an action.

    :param pack_name: Content pack name.
    :type pack_name: ``str``
    :param entry_point: Action entry point.
    :type entry_point: ``str``

    :rtype: ``str``
    """
    entry_point_abs_path = get_entry_point_abs_path(pack=pack, entry_point=entry_point)
    if entry_point_abs_path is not None:
        return os.path.join(os.path.dirname(entry_point_abs_path), ACTION_LIBS_DIR)
    else:
        return None


def get_aliases_base_paths():
    """
    Return a list of base paths which are searched for action aliases.

    :rtype: ``list``
    """
    aliases_base_paths = cfg.CONF.content.aliases_base_paths or ''

    # Remove trailing colon (if present)
    if aliases_base_paths.endswith(':'):
        aliases_base_paths = aliases_base_paths[:-1]

    result = []

    aliases_base_paths = aliases_base_paths.split(':')

    result = aliases_base_paths
    result = [path for path in result if path]
    result = list(OrderedSet(result))
    return result
