#!/bin/sh
cd "$(sim_db get $@)"
source /Users/hakonaustlidtasken/.bash_profile
exec bash
