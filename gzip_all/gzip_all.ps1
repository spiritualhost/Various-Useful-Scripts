#Create a compressed tarball for every file in a directory

#Define parameters - get user to give directory
param(
    [Parameter(Mandatory=$true)]
    [string]$Directory
)

#Exit script if no args passed or if directory doesn't exist
if (-not (Test-Path -Path $Directory -PathType Container)){
    Write-Error "Directory '$Directory' does not exist."
    exit 1
}

#Change to directory and throw error if issue
try {
    Push-Location -Path $Directory    
}
catch {
    <#Do this if a terminating exception happens#>
    Write-Error "Failed to change directory to '$Directory'. $_"
    exit 1
}


#For all files in directory, compress to tarball
    foreach ($file in Get-ChildItem -File){

        $filename = $file.Name

        $archivename = "$filename.tar.gz"

        Write-Host "$filename has been found."
            
        Write-Host "$filename is transforming into $archivename."

        tar -czvf $archivename -- "$filename"

        #Error handling for compression issues (If last error code not equal to 0)
        
        if ($LASTEXITCODE -ne 0){
            Write-Error "Compression failed for '$filename'"
        }
    }


#Testing
#Uncomment this to have the script run on the provided test/ directory and then pop out
#Set-Location ..