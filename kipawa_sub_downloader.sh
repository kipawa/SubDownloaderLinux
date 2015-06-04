tmp=$IFS
IFS="
"

path=$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
exe="~/Desktop/SubDownloader/dist/subdwnld"
cd ~Desktop/SubDownloader/dist
./subdwnld $path

#echo "Naya" > path.txt
#echo $path >> path.txt
#opensubtitles-download 3.2
IFS=$tmp
