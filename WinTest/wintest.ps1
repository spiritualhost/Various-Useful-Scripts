#Flags
param(
    [switch]$v,
    [switch]$verbose,
    [switch]$r,
    [switch]$remote
)

#Set variables to base value (False)
$SBoot = $TPM = $CPU = $MEM = $STOR = $CORES = $CLK = $BIT = 0

#Check for Secure Boot Capability
if (Confirm-SecureBootUEFI) {
    $SBoot = 1
}

#Check that TPM 2.0 is supported and enabled
$TPM_VER = (tpmtool getdeviceinformation | Select-String "TPM Version").ToString().Split(":")[1].Trim()
if (($TPM_VER -eq "2.0") -and ((Get-Tpm).TpmPresent -eq 1) -and ((Get-Tpm).TpmEnabled -eq 1)) {
    $TPM = 1
}

#Check that the processor is supported for Windows 11
#This requires checking from the list intel.txt, which is contained in the root folder
#Source: https://learn.microsoft.com/en-us/windows-hardware/design/minimum/windows-processor-requirements
$supportedCPUs = Get-Content "intel.txt"
$modelNum = (Get-CimInstance Win32_Processor).Name -match '\b\w+-\d+\w*\b' | Out-Null; $Matches[0]
if ($supportedCPUs -contains $modelNum) {
    $CPU = 1
}

#Check that there is at least 4GB of system memory
$RAM = ((Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property capacity -Sum).sum / 1GB)
if ($RAM -gt 4) {
    $MEM = 1
}

#Check that the system disk is 64 GB or larger
$DriveLetter = Split-Path -Path $pwd.Path -Qualifier
$Volume = Get-CimInstance -Class Win32_Volume -Filter "DriveLetter='$DriveLetter'"
if (($Volume.Capacity)/1GB -gt 64) {
    $STOR = 1
}

#Check that the processor has two or more cores
if ((Get-CimInstance -ClassName Win32_Processor).NumberOfCores -gt 2) {
    $CORES = 1
}

#Check that the processor has a base clock speed greater than 1 Ghz
$CLK_SPD = (Get-CimInstance Win32_Processor | Select-Object -ExpandProperty MaxClockSpeed)/1000

if ($CLK_SPD -gt 1.0) {
    $CLK = 1
}

#Check that the processor is x64
$BITSIZE = (Get-CimInstance Win32_Processor).Architecture

if ($BITSIZE -eq 9) {
    $BIT = 1
}

#Only write to terminal if verbose
if ($v -or $verbose){
    #Return results
    if ($SBoot * $TPM * $CPU * $MEM * $STOR * $CORES * $CLK * $BIT -eq 1){ 
        Write-Output "This Computer is Eligible for an Upgrade to Windows 11."
        Write-Output ""
    }
    else {
        Write-Output "This Computer is not Eligible for Windows 11. Please see results below for more information:"
        Write-Output ""
        Write-Output "Results:"
        Write-Output "~~~~~~~~~~~~~~~~~~~"
        Write-Output "Secure Boot: $SBOOT"
        Write-Output "TPM: $TPM"
        Write-Output "CPU Model Approved: $CPU"
        Write-Output "CPU Cores: $CORES"
        Write-Output "Clock Speed: $CLK"
        Write-Output "Bit Size (x64): $BIT"
        Write-Output "Memory (RAM): $MEM"
        Write-Output "Storage Capacity: $STOR"
    }
}

#Send the output to a remote server as an api call
elseif ($r -or $remote) {
    $hostname = "$env:COMPUTERNAME"
    $parameters =  "$SBOOT$TPM$CPU$CORES$CLK$BIT$MEM$STOR"

    Start-Process "https://192.168.200.xxx:5000/eligible?hostname=$hostname&parameters=$parameters"
}