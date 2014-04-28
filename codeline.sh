#!/usr/bin/env sh
find /home/jeanlyn/autopro/webapp/ \( -path '*/cluster*' -o -path '*/agentservice/cluster*' \) -a -prune -o -type f -regex ".*\(\.py\|\.sh\|\.html\)"|xargs cat 2>/dev/null|wc -l