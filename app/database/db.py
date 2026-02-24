from typing import List, Dict, Optional
from datetime import datetime
import aiosqlite


class Database:
    def __init__(self, db_file="muscles.db"):
        self.db_name = db_file
        self.con = None

    async def connect(self) -> None:
        """Call this method when starting bot to initialize the DB."""
        self.con = await aiosqlite.connect(self.db_name)
        await self.__create_table()

    async def __create_table(self) -> None:
        cursor = await self.con.execute("""
            CREATE TABLE IF NOT EXISTS user_muscles (
                user_id INTEGER,
                muscle TEXT,
                last_trained TEXT,
            )
        """)
        await cursor.close()
        await self.con.commit()

    async def add_user(self, user_id: int) -> bool:
        """Adds a default set of muscles for a new user. Returns false upon failure."""
        default_muscles = [
            "Biceps", "Triceps", "Back", "Forearms", 
            "Shoulders", "Leg Biceps", "Back of leg", "Trapezius"
        ]
        
        data = [(user_id, muscle) for muscle in default_muscles]
        
        try:
            cursor = await self.con.executemany(
                "INSERT OR IGNORE INTO user_muscles (user_id, muscle) VALUES (?, ?)", 
                data
            )
            await cursor.close()
            await self.con.commit()
            return True
        except Exception as e:
            print(f"Database error in add_user: {e}")
            return False

    async def add_user_muscle(self, user_id: int, muscle_name: str) -> bool:
        """Adds a new muscle for the user to track. Returns false upon failure."""
        try:
            cursor = await self.con.execute(
                "INSERT OR IGNORE INTO user_muscles (user_id, muscle) VALUES (?, ?)", 
                (user_id, muscle_name)
            )
            await cursor.close()
            await self.con.commit()

            self.update_user_muscle(user_id, muscle_name)
            return True
        except Exception as e:
            print(f"Database error in add_user_muscle: {e}")
            return False

    async def get_users(self) -> List[int]:
        """Returns list of all unique user ids"""
        cursor = await self.con.execute("SELECT DISTINCT user_id FROM user_muscles")
        rows = await cursor.fetchall()
        await cursor.close()

        return [row[0] for row in rows]
    
    async def get_user_muscles(self, user_id: int) -> Dict[str, Optional[datetime]]:
        """Returns muscles user trains and time last trained."""
        cursor = await self.con.execute(
            "SELECT muscle, last_trained FROM user_muscles WHERE user_id = ?", 
            (user_id,)
        )
        rows = await cursor.fetchall()
        await cursor.close()
        
        result = {}
        for muscle, last_trained_str in rows:
            if last_trained_str:
                result[muscle] = datetime.fromisoformat(last_trained_str)
            else:
                result[muscle] = None
                
        return result
    
    async def update_user_muscle(self, user_id: int, muscle_name: str) -> bool:
        """Sets last_trained date to current time. Returns false upon failure."""
        try:
            now = datetime.now().isoformat()
            
            cursor = await self.con.execute(
                "UPDATE user_muscles SET last_trained = ? WHERE user_id = ? AND muscle = ?",
                (now, user_id, muscle_name)
            )
            rowcount = cursor.rowcount
            await cursor.close()
            await self.con.commit()
            
            return rowcount > 0 
        except Exception as e:
            print(f"Database error in update_user_muscle: {e}")
            return False


db = Database()
