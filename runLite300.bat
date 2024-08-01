d:
cd d:\HFSMOL
call .\venv\Scripts\activate.bat
start cmd.exe /k .\llamafile-0.8.12.exe -m .\models\Lite-Oute-1-300M-Instruct-Q8_0.gguf -c 4096 --host 0.0.0.0 --nobrowser
streamlit run .\st-Lite300M-llamafile.py


PAUSE