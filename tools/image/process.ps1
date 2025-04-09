python tools/image/resize.py assets/resource/base/image/Items assets/resource/base/image/Items_resized --width 113 --height 113

python tools/image/crop.py assets/resource/base/image/Items_resized assets/resource/base/image/Items_cropped --box 16 12 82 57

python tools/image/transparency2green.py assets/resource/base/image/Items_cropped assets/resource/base/image/Items_processed

Remove-Item -Path "assets/resource/base/image/Items_resized" -Recurse -Force
Remove-Item -Path "assets/resource/base/image/Items_cropped" -Recurse -Force

Write-Host "Process Completed" -ForegroundColor Green