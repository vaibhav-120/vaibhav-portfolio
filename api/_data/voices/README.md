Piper voice models go here. From the project root, run:

    sh scripts/download-voice.sh

That saves `en_US-lessac-medium.onnx` and `en_US-lessac-medium.onnx.json`.
Commit both files so Vercel deploys them with the function.

Without a voice file, the agent still works: the browser speaks the answers
with its built-in voice instead.
