from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class UserState:
    state: str
    bucket_name: Optional[str] = None
    face_name: Optional[str] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class UserStateManager:
    def __init__(self):
        self._states = {}
        self._ttl = 3600  # 1 час время жизни состояния
    
    def set_state(self, user_id: int, state: str, bucket_name: str = None, face_name: str = None):
        self._states[user_id] = UserState(
            state=state, 
            bucket_name=bucket_name, 
            face_name=face_name
        )
    
    def get_state(self, user_id: int) -> Optional[UserState]:
        state = self._states.get(user_id)
        if state and time.time() - state.created_at > self._ttl:
            self.clear_state(user_id)
            return None
        return state
    
    def clear_state(self, user_id: int):
        self._states.pop(user_id, None)


user_state_manager = UserStateManager()