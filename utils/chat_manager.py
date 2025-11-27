import json
import os
from datetime import datetime

class ChatManager:
    """Manages persistent chat history storage"""
    
    def __init__(self, storage_file="chat_history.json"):
        self.storage_file = storage_file
        self.ensure_storage_exists()
    
    def ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"conversations": []}, f)
    
    def save_conversation(self, messages, session_id=None):
        """Save current conversation to storage"""
        if not messages:
            return
        
        try:
            # Load existing data
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Create conversation object
            conversation = {
                "id": session_id or datetime.now().strftime("%Y%m%d_%H%M%S"),
                "timestamp": datetime.now().isoformat(),
                "messages": messages,
                "message_count": len(messages)
            }
            
            # Add to conversations list
            data["conversations"].append(conversation)
            
            # Keep only last 10 conversations to prevent file bloat
            if len(data["conversations"]) > 10:
                data["conversations"] = data["conversations"][-10:]
            
            # Save back to file
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def load_all_conversations(self):
        """Load all saved conversations"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            return data.get("conversations", [])
        except Exception as e:
            print(f"Error loading conversations: {e}")
            return []
    
    def load_conversation(self, conversation_id):
        """Load a specific conversation by ID"""
        conversations = self.load_all_conversations()
        for conv in conversations:
            if conv["id"] == conversation_id:
                return conv["messages"]
        return None
    
    def get_conversation_summary(self):
        """Get summary of all conversations"""
        conversations = self.load_all_conversations()
        summaries = []
        
        for conv in conversations:
            summary = {
                "id": conv["id"],
                "timestamp": conv["timestamp"],
                "message_count": conv["message_count"],
                "preview": conv["messages"][0]["content"][:50] + "..." if conv["messages"] else "Empty"
            }
            summaries.append(summary)
        
        return summaries
    
    def delete_conversation(self, conversation_id):
        """Delete a specific conversation"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Filter out the conversation
            data["conversations"] = [
                conv for conv in data["conversations"] 
                if conv["id"] != conversation_id
            ]
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    def clear_all_history(self):
        """Clear all conversation history"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump({"conversations": []}, f)
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False