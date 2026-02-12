param(
    [string]$OutputDir = "$env:USERPROFILE\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\www.govinfo.gov_bulkdata_ECFR_title-21",
    [int]$TitleNumber = 21,
    [int]$PartNumber = 211
)

$ErrorActionPreference = 'Stop'

$titlesUrl = 'https://www.ecfr.gov/api/versioner/v1/titles.json'
Write-Host "Fetching title metadata from: $titlesUrl"

$titles = Invoke-RestMethod -Uri $titlesUrl -Method Get
$title = $titles.titles | Where-Object { $_.number -eq $TitleNumber } | Select-Object -First 1

if (-not $title) {
    throw "Title $TitleNumber was not found in eCFR titles metadata."
}

$asOf = $title.up_to_date_as_of
if (-not $asOf) {
    throw "up_to_date_as_of is missing for title $TitleNumber."
}

Write-Host "Latest snapshot date for Title ${TitleNumber}: $asOf"

$xmlUrl = "https://www.ecfr.gov/api/versioner/v1/full/$asOf/title-$TitleNumber.xml?part=$PartNumber"

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

$fileName = "title-$TitleNumber`_part-$PartNumber`_$asOf.xml"
$outPath = Join-Path $OutputDir $fileName

if (Test-Path $outPath) {
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $outPath = Join-Path $OutputDir ("title-$TitleNumber`_part-$PartNumber`_$asOf`_$stamp.xml")
}

Write-Host "Downloading Part $PartNumber XML from: $xmlUrl"
Invoke-WebRequest -Uri $xmlUrl -OutFile $outPath

Write-Host "Saved: $outPath"
