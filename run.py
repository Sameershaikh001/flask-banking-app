import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Get port from environment variable (for Render/GitHub Actions)
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 to accept connections from outside the container
    app.run(host="0.0.0.0", port=port, debug=False)