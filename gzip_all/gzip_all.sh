#Create a compressed tarball for every file in a directory

#Exit script if no args passed
[ $# -lt 1 ] && echo "Usage: $0 <zipdir>" && exit 1

#Take in args from user input
DIRECTORY="$1"

#Change to directory and throw error if issue
cd "$DIRECTORY" || { echo "Cannot cd into $LOGDIR"; exit 1; }

for file in *; do 
    #Check that compressed item is file, not folder
    [ -f "$file" ] || continue

    echo "$file is being zipped"
    tar -czf "$file.tar.gz" "$file"
done