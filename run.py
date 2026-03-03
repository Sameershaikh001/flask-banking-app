import os
import threading
import time
import requests
from datetime import datetime
from app import create_app

app = create_app()

def start_ping_loop():
    """Background thread to ping the app every 30 seconds to keep it alive on Render."""
    render_url = os.environ.get('RENDER_EXTERNAL_URL')
    if not render_url:
        app.logger.warning("RENDER_EXTERNAL_URL not set. Keep-alive thread not started.")
        return

    def ping_server():
        with app.app_context():
            while True:
                try:
                    start_time = time.time()
                    response = requests.get(render_url, timeout=10)
                    ping_time = (time.time() - start_time) * 1000
                    app.logger.info(
                        f"Keep-alive | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                        f"Status: {response.status_code} | Latency: {ping_time:.2f}ms"
                    )
                except requests.exceptions.RequestException as e:
                    app.logger.error(f"Keep-alive request failed: {str(e)}")
                except Exception as e:
                    app.logger.error(f"Unexpected keep-alive error: {str(e)}")
                finally:
                    time.sleep(30)

    if not app.debug:
        thread = threading.Thread(target=ping_server, daemon=True)
        thread.start()
        app.logger.info(f"Keep-alive service started for {render_url}")
    else:
        app.logger.info("Debug mode: keep-alive not started")

# Start the keep-alive loop
start_ping_loop()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)