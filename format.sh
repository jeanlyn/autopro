#!/bin/bash
if [ "$#" -ne 1 ]
    then
        echo "just need one args"
        exit
    fi
#sed '/^$/d' $1 > $2
#sed 's/^<property>/    <property>/;s/^<name>/        <name>/;s/^<value>/        <value>/;s/^<\/property>/    <\/property>/;' $2 > $1
#rm $2
xmllint --format $1 > ${1}.jeanlyn
mv ${1}.jeanlyn $1
