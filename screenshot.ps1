Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $bounds.width, $bounds.height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.size)
$bitmap.Save("C:\Users\ASUS\Downloads\000000-Workshop\000058-SessionManager\static\images\WorklogT4\lab13-test-restore.png")
$graphics.Dispose()
$bitmap.Dispose()
