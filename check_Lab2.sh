#!/bin/sh

if grep ^'student:' /etc/passwd > /dev/null
then
    if grep ^'student ALL=(ALL:ALL) ALL'$ /etc/sudoers > /dev/null
	then
        a1=50
		echo $a1
	else
	echo "0"
	fi
else
echo "0"
fi

if grep ^'root:x:0:0:root:/root:/bin/false'$ /etc/passwd > /dev/null
then
a2=50
	echo $a2
else
echo "0"
fi

