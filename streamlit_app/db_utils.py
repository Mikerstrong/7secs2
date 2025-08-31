import json
import os
import time
import tempfile


def load_db(db_path):
    """Safely load a JSON DB file. Returns None on any error/corruption.
    Also checks fallback location in user's home directory."""
    # Try primary location first
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Corrupt or partially-written file; try fallback
            pass
    
    # Try fallback location if primary fails
    try:
        home_dir = os.path.expanduser("~")
        fallback_dir = os.path.join(home_dir, ".7secs2_data")
        fallback_path = os.path.join(fallback_dir, os.path.basename(db_path))
        
        if os.path.exists(fallback_path):
            with open(fallback_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        # Both primary and fallback failed
        pass
    
    # Return None if all attempts failed
    return None


def save_db(db_path, data):
    """Atomically save JSON to avoid corruption on crashes."""
    home_dir = os.path.expanduser("~")
    fallback_dir = os.path.join(home_dir, ".7secs2_data")
    fallback_path = os.path.join(fallback_dir, os.path.basename(db_path))
    
    def try_save_to_path(target_path):
        """Try to save to a specific path atomically."""
        try:
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # Create temp file in the same directory as target
            tmp_fd, tmp_path = tempfile.mkstemp(prefix=".tmp_db_", dir=target_dir)
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                
                # Atomically replace the target file
                os.replace(tmp_path, target_path)
                return True
            finally:
                # Clean up temp file if it still exists
                try:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except (OSError, PermissionError):
                    pass
        except (OSError, PermissionError, Exception):
            return False
    
    # Try to save to original location first
    if try_save_to_path(db_path):
        return
    
    # If that fails, try the fallback location
    if try_save_to_path(fallback_path):
        return
    
    # If both fail, log the error but don't crash
    print(f"Failed to save database to both {db_path} and {fallback_path}")
    
    # As a last resort, try to save without atomic operation
    try:
        os.makedirs(fallback_dir, exist_ok=True)
        with open(fallback_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Final fallback save failed: {e}")
