#!/bin/bash
# taken grom xbmc-czech-sf.net
TOOLS=$(dirname "$0")"/tools"


BUILD_DIR=tmp
PUBLISH_DIR=repo
mkdir -p ${BUILD_DIR}

if [ -z $1 ];
then
  echo "use -n to release addons that need it"
  exit 0
elif [ "$1" == "-n" ];
then
  echo "Determining which addons need to be released"
  addons=$(python addons.py | grep Addon | gawk -F' ' '{print $2}')
else
	addons=$1
fi
echo "Updating addon submodules"
git submodule foreach git pull origin master

echo "Cleaning up *.pyc files.."
find . -name '*.pyc' | xargs rm -f

if [ ! "$addons" ];
then
  exit 0
fi

for addonFile in $addons ; do
    dirname=$addonFile
    if [ ! -f $addonFile/addon.xml ] ; then
	#echo "$addonFile/addon.xml does not exist, skipping"
	continue
    fi
    addon_id=$("$TOOLS/get_addon_attribute" "$addonFile/addon.xml" "id")
    addon_version=$("$TOOLS/get_addon_attribute" "$addonFile/addon.xml" "version")

    if [ -z "$addon_id" ] ; then
        echo "Addon id not found!" >&2
        exit 1
    fi

    if [ -z "$addon_version" ] ; then
        echo "Addon id not found!" >&2
        exit 2
    fi

    target_dir="$BUILD_DIR/$addon_id"
    if [ ! -d "$target_dir" ] ; then
        mkdir "$target_dir"
    fi

    echo "Packing $addon_id $addon_version"

    # make package
    package="$target_dir/$addon_id-$addon_version.zip"
    if [ -e "$package" ] ; then
        rm "$package"
    fi
    zip -FS -q -r "$package" "$dirname" -x "*.py[oc] *.sw[onp]" ".*"

    # copy changelog file
    changelog=$(ls "$dirname"/[Cc]hangelog.txt)
    if [ -f "$changelog" ] ; then
        cp "$changelog" "$target_dir"/changelog-$addon_version.txt
    fi

    # copy icon file
    icon="$dirname"/icon.png
    if [ -f "$icon" ] ; then
        cp "$icon" "$target_dir"/
    fi
    git stash
    git checkout gh-pages
    mkdir -p $PUBLISH_DIR/$addon_id
    mv $target_dir/* $PUBLISH_DIR/$addon_id/
    git add $PUBLISH_DIR/$addon_id
    git commit -m "Release $addon_id $addon_version"
    git checkout master
    git stash pop
done 
echo "Regenerate addons.xml"
python repo_generator.py
git stash
git checkout gh-pages
mv tmp/addons.xml* repo
./update-directory-index.sh
git add repo
git commit -m 'Update metadata files'
git checkout master
git stash pop
echo "Done"
