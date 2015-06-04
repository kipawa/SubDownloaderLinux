tmp=$IFS
IFS="
"

path=$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
exe="/home/kipawa/SubDownloader/dist/subdwnld"
cd /home/kipawa/SubDownloader/dist
./subdwnld $path

#echo "Naya" > path.txt
#echo $path >> path.txt
#opensubtitles-download 3.2
IFS=$tmp