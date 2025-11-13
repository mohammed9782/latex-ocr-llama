FROM ollama/ollama:latest

# Copy the wait-and-pull helper and make it executable
COPY wait-and-pull.sh /wait-and-pull.sh
RUN chmod +x /wait-and-pull.sh

# Run the helper script (it will use the ollama CLI inside the image)
ENTRYPOINT ["/wait-and-pull.sh"]
