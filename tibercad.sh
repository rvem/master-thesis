#! /usr/bin/env bash

set -euo pipefail

tib_file="$1"
tib_file_dir="$(dirname "$tib_file")"
tib_file_name="$(basename "$tib_file")"
user_id="$(id -u)"
tibercad_cmd=("ls && tibercad $tib_file_name && useradd -u $user_id user && chown -R $user_id:users .")
docker run -v "$PWD/$tib_file_dir:/data" tibercad bash -c "${tibercad_cmd[*]}"
