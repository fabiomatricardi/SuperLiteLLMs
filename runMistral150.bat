d:
cd d:\HFSMOL
call .\venv\Scripts\activate.bat
start cmd.exe /k .\llamafile-0.8.12.exe -m .\models\Lite-Mistral-150M-v2-Instruct-Q8_0.gguf -c 2048 --host 0.0.0.0 --nobrowser
streamlit run .\st-LiteMistral150M-llamafile.py


PAUSE