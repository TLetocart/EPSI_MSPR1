# Configuration
$repoUser = "TLetocart"
$repoName = "EPSI_MSPR1"
$installPath = "C:\Users\tom96\OneDrive\Documents\COURS\MSPR1"
$archiveName = "$installPath\latest_release.zip"

Write-Host "Verification de la derniere version publiee..."

# ----------------------- Connexion Github --------------------------- #

$latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/$repoUser/$repoName/releases/latest"

if (-not $latestRelease) {
    Write-Host "Aucune release trouvee."
    exit
}

# Vérifie si des fichiers sont attachés a la release, sinon, telecharge le zip du depot
if ($latestRelease.assets.Count -gt 0) {
    $latestReleaseUrl = $latestRelease.assets[0].browser_download_url
} else {
    Write-Host "Aucun fichier attache a la release, téléchargement du ZIP du dépôt..."
    $latestReleaseUrl = $latestRelease.zipball_url
}

Write-Host "Telechargement depuis $latestReleaseUrl ..."
Invoke-WebRequest -Uri $latestReleaseUrl -OutFile $archiveName


# ---------------------------------------------------------------------------------


if (-not $latestReleaseUrl) {
    Write-Host "Impossible de recuperer la dernière release."
    exit
}


Write-Host "Telechargement de la mise à jour..."
Invoke-WebRequest -Uri $latestReleaseUrl -OutFile $archiveName

if (-not (Test-Path $archiveName)) {
    Write-Host "Echec du telechargement."
    exit
}

Write-Host "Extraction de la mise à jour..."
Expand-Archive -Path $archiveName -DestinationPath $installPath -Force

Write-Host "Nettoyage des fichiers temporaires..."
Remove-Item -Path $archiveName -Force

Write-Host "Mise a jour terminee avec succes "