#!/bin/bash

dir_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )

psql -f "$dir_path/db_clear.sql" testing_trotto_core
