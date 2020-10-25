# this is a log of command run using azure CLI
$resourceGroup = "BitjunctionAcr"
az group create -n $resourceGroup -l westeurope
$registryName = "bitjunctionacr"
az acr create -g $resourceGroup -n $registryName --sku Basic --admin-enabled true