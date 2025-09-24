"""Nightly snapshot job."""

import asyncio
from datetime import datetime, date
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.snapshots import SnapshotsService


async def run_nightly_snapshot() -> None:
    """Run nightly portfolio snapshot for all users."""
    db = next(get_db())
    
    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()
        
        snapshots_service = SnapshotsService(db)
        
        for user in users:
            try:
                # Create snapshot for user
                snapshot = snapshots_service.create_daily_snapshot(user.id)
                
                # In production, save to snapshots table
                # For now, just log the snapshot
                print(f"Snapshot for user {user.id}: {snapshot.total_value} (G/L: {snapshot.gain_loss_percent:.2f}%)")
                
            except Exception as e:
                print(f"Error creating snapshot for user {user.id}: {e}")
        
        print(f"Completed nightly snapshots for {len(users)} users")
        
    except Exception as e:
        print(f"Error in nightly snapshot job: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(run_nightly_snapshot())
