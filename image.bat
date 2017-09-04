set fn=E:\ImageMagick-6.9.1-Q16\convert.exe
for /f "tokens=*" %%i in ('dir/s/b *.png') do "%fn%" "%%i" -strip "%%i"
pause
python -m py_compile analog.py