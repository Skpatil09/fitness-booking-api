import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def load_seed_data():
    # Open and read the JSON file
    with open('seed_data.json', 'r') as f:
        classes_data = json.load(f)

    db: Session = SessionLocal()

    try:
        for class_item in classes_data:
            # Convert datetime string to Python datetime object
            class_datetime = datetime.fromisoformat(class_item['datetime'])

            # Create FitnessClass instance
            fitness_class = models.FitnessClass(
                id=class_item['id'],
                name=class_item['name'],
                datetime=class_datetime,
                instructor=class_item['instructor'],
                total_slots=class_item['total_slots'],
                available_slots=class_item['available_slots']
            )

            # Add to session
            db.merge(fitness_class)  # merge to avoid duplicates if rerun

        # Commit all changes
        db.commit()
        print("Seed data loaded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error loading seed data: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    load_seed_data()
