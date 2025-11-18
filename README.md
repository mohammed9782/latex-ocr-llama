# LlamaTeX: Image-to-Equation Converter

Extract LaTeX code from images using the Llama 3.2 Vision model via Ollama and Streamlit.

## Overview

This project provides a user-friendly web interface (built with Streamlit) that leverages Ollama and the Llama 3.2 Vision model to automatically extract LaTeX mathematical equations from images. Upload an image containing mathematical formulas, and the app will use the vision model to recognize and output the corresponding LaTeX code.

### Key Features
- 🖼️ **Image Upload**: Upload PNG, JPG, or JPEG images.
- 🦙 **Llama 3.2 Vision**: Uses state-of-the-art vision model for accurate OCR.
- 📝 **LaTeX Extraction**: Outputs clean, compilable LaTeX code without extra formatting.
- 🎨 **Rendered Preview**: View the LaTeX rendered as formatted equations.
- 🐳 **Docker Support**: Easy deployment with Docker Compose.
- 💾 **Persistent Storage**: Models and data persisted across restarts.

---

## Project Structure

```
latex-ocr-llama/
├── app.py                          # Main Streamlit application
├── Dockerfile                      # Streamlit container build
├── docker-compose.yml              # Multi-container orchestration
├── environment.yml                 # Conda environment specification
├── requirements.txt                # Python dependencies (pip)
├── tools/
│   └── ollama-puller/
│       ├── Dockerfile              # Helper image for model download
│       └── wait-and-pull.sh         # Script to wait for server & pull model
└── README.md                        # This file
```

---

## Getting Started

### Option 1: Docker Compose (Recommended for Production/Testing)

#### Prerequisites
- Docker and Docker Compose installed on your system.
- ~15 GB free disk space (for the Llama 3.2 Vision model).
- ~12 GB available RAM (Llama 3.2 Vision requires significant memory).

#### Deployment Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mohammed9782/latex-ocr-llama.git
   cd latex-ocr-llama
   ```

2. **Start the Services**
   ```bash
   docker compose up --build
   ```
   This will:
   - Build the Streamlit app image.
   - Build the Ollama model puller helper image.
   - Start the Ollama server and wait for it to be ready.
   - Download and cache the `llama3.2-vision` model (~8 GB).
   - Launch the Streamlit web interface.

3. **Access the Application**
   - Open your browser and navigate to: `http://localhost:8501`
   - Upload an image and click "Extract LaTeX Code".

4. **Stop the Services**
   ```bash
   docker compose down
   ```
   Use `docker compose down -v` to also remove volumes (note: this will delete cached models).

#### How It Works

- **ollama_server**: Runs the Ollama HTTP API server on port 11434.
- **ollama-pull**: A helper service that waits for the server to be ready, then pulls and caches the `llama3.2-vision` model.
- **latex_ocr_app**: Streamlit web app that communicates with Ollama to process images.

All services share a named Docker network (`app_network`) and a persistent volume (`ollama_data`) for model caching.

#### Troubleshooting Docker Deployment

- **"Port 11434 already in use"**: Another process or container is using the port. Either stop it or change the port in `docker-compose.yml` (e.g., `11435:11434`).
- **Model download timeout**: Increase the `MAX` environment variable in `docker-compose.yml` for `ollama-pull` (e.g., `MAX: 600` for 10 minutes).
- **Out of memory**: Ensure your system has at least 4 GB RAM available. Reduce background processes or increase virtual memory if needed.

---

### Option 2: Conda Environment (Development Setup)

#### Prerequisites
- Anaconda or Miniconda installed.
- Python 3.10+.
- ~12 GB available RAM (Llama 3.2 Vision requires significant memory).
- Ollama installed and running locally (see [Ollama Installation](https://ollama.ai)).

#### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mohammed9782/latex-ocr-llama.git
   cd latex-ocr-llama
   ```

2. **Create Conda Environment**
   ```bash
   conda env create -f environment.yml
   ```
   This creates an environment named `latex-ocr-llama` with all dependencies.

3. **Activate the Environment**
   ```bash
   conda activate latex-ocr-llama
   ```

4. **Start Ollama Server (in a separate terminal)**
   ```bash
   ollama serve
   ```
   By default, this listens on `http://localhost:11434`.

5. **Pull the Model (in another terminal)**
   ```bash
   ollama pull llama3.2-vision
   ```
   Wait for the download to complete (~8 GB).

6. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```
   The app will open in your browser at `http://localhost:8501`.

#### Environment Details

The `environment.yml` specifies:
- **Python 3.10**
- **Streamlit**: Web app framework.
- **Ollama**: LLM and vision model inference (client library).
- **Pillow (PIL)**: Image processing.

#### Deactivate Environment
```bash
conda deactivate
```

---

## Usage

### Via Web Interface (Both Docker & Conda)

1. **Upload Image**: Click "Choose an image..." and select a PNG, JPG, or JPEG file containing mathematical equations.
2. **View Preview**: The uploaded image is displayed in the sidebar.
3. **Extract LaTeX**: Click the "Extract LaTeX Code" button (blue, primary style).
4. **View Results**:
   - **Extracted LaTeX Code**: Displayed as a syntax-highlighted code block.
   - **Rendered Equation**: Displayed as formatted LaTeX below the code.
5. **Clear Results**: Click the "Clear 🗑️" button to reset and start fresh.

### Example

**Input Image**: A handwritten or printed equation like `∑(x² + 2x + 1)`.

**Output LaTeX**:
```latex
\sum (x^{2} + 2x + 1)
```

**Rendered**: The equation is displayed in mathematical typeset format.

---

## API Details

### Ollama Integration

The app communicates with the Ollama server using the `/api/chat` endpoint:

```python
response = ollama.chat(
    model="llama3.2-vision",
    messages=[{
        'role': 'user',
        'content': 'Extract LaTeX from this image...',
        'images': [image_bytes]
    }]
)
```

### Configuration

#### Docker
Set via `docker-compose.yml`:
- `OLLAMA_HOST`: URL of Ollama server (default: `http://ollama:11434`).
- `LLM_MODEL`: Model to use (default: `llama3.2-vision`).
- `MAX`: Timeout for model pull in seconds (default: `60`).

#### Conda / Local
Set environment variables before running:
```bash
export OLLAMA_HOST=http://localhost:11434
export LLM_MODEL=llama3.2-vision
streamlit run app.py
```

---

## Performance Considerations

- **Model Size**: ~8 GB disk space for `llama3.2-vision`.
- **Memory Requirements**: ~12 GB RAM (Llama 3.2 Vision is memory-intensive).
- **Inference Speed**: ~10–30 seconds per image on CPU (varies with image size and system specs).
- **GPU**: Not required but recommended for faster inference (NVIDIA CUDA supported by Ollama).

---

## Customization

### Change the Model

To use a different Ollama model (e.g., `llava`, `gpt4v-equivalent`):

1. **Update docker-compose.yml** or environment:
   ```yaml
   environment:
     MODEL: llava  # or another model
   ```

2. **Or via env variable**:
   ```bash
   export LLM_MODEL=llava
   ```

3. **Modify the prompt** in `app.py` (line ~49) if needed for the new model.

### Add Authentication

To add basic HTTP auth to Streamlit:

```bash
streamlit run app.py --logger.level=debug
```

Or use a reverse proxy (e.g., Nginx) with authentication in front of the app.

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"ollama server not responding"** | Ensure Ollama is running (`ollama serve` or Docker service is up). |
| **Model download hangs** | Increase `MAX` timeout; check internet connection. |
| **"Port X already in use"** | Stop conflicting process or change port in `docker-compose.yml`. |
| **Out of memory errors** | Ensure 12GB+ RAM available; close other applications; consider swap or GPU acceleration. |
| **Slow inference** | Expected on CPU; consider GPU setup or accept longer response times. |

### Debug Mode

Enable Streamlit debug logs:
```bash
streamlit run app.py --logger.level=debug
```

View Docker logs:
```bash
docker compose logs -f ollama
docker compose logs -f streamlit-app
```

---

## Credits

This project is built upon and inspired by:

- **[AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub)**: Raw source code and foundational concepts for the OCR pipeline and Streamlit integration.
- **[Ollama](https://ollama.ai)**: LLM and vision model serving infrastructure.
- **[Llama 3.2 Vision](https://www.llama.com)**: Vision model by Meta.
- **[Streamlit](https://streamlit.io)**: Web app framework.

---

## License

This project is provided as-is for educational and learning purposes. Refer to the original sources (especially the [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub)) for their respective licenses.

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues.
- Suggest features or improvements.
- Submit pull requests.


---

## Deployment

For cloud deployment options (Railway, Fly.io, AWS, etc.), see the inline comments in `docker-compose.yml` or contact the maintainers.

---

**Happy LaTeX extraction! 🦙📝**
