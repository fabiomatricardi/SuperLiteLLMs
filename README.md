# SuperLiteLLMs
super Lite LLMs


```
mkdir HFSmol_LM

cd HFSmol_LM
python -m venv venv

venv\Scripts\activate

deactivate

pip install streamlit==1.36.0 openai tiktoken


Download llamafile
wget https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.12/llamafile-0.8.12 -OutFile llamafile-0.8.12.exe


download the weights
mkdir models
cd models

wget https://huggingface.co/MaziyarPanahi/SmolLM-135M-Instruct-GGUF/resolve/main/SmolLM-135M-Instruct.Q8_0.gguf -OutFile SmolLM-135M-Instruct.Q8_0.gguf

wget https://huggingface.co/MaziyarPanahi/SmolLM-360M-Instruct-GGUF/resolve/main/SmolLM-360M-Instruct.Q8_0.gguf -OutFile SmolLM-360M-Instruct.Q8_0.gguf

```

### to run

```

.\llamafile-0.8.12.exe -m .\models\Lite-Mistral-150M-v2-Instruct-Q8_0.gguf -c 2048 --host 0.0.0.0 --nobrowser
streamlit run .\st-LiteMistral150M-llamafile.py

```
