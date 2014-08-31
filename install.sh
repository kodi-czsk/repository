for addon in $(ls -l | grep "^d" | gawk -F' ' '{print $9}') ; do
	dirname=$addon
	if [ -f $addon/install.sh ] ; then
		cd $addon
		echo "$addon : ./install.sh"
		./install.sh
		cd ..
	fi
done
