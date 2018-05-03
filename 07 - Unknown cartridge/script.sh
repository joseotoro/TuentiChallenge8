#!/bin/bash

result="$(strings unknown | head -n 2 | tail -n 1 | base64 --decode | awk '{ for (i=NF; i>1; i--) printf("%s ", $i); print $1; }')"

echo "Paste this into https://www.dcode.fr/pikalang-language:"
echo $result;