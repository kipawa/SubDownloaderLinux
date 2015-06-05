#IFS refers to Internal Field Seperator, which is by default set to space. We must set it to new line!
tmp=$IFS
IFS="
"

path=$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
cd ~/Desktop/SubDownloader/dist
./subdwnld $path

IFS=$tmp
# ^ We have restored the value of IFS
