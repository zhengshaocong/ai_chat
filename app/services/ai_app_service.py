from app.models.models import AIApp

class AIAppService:
    def get_all_ai_apps(self, db):
        return db.query(AIApp).all()

    def get_ai_app_by_id(self, db, app_id):
        return db.query(AIApp).filter(AIApp.id == app_id).first()

    def create_ai_app(self, db, name, description, icon):
        ai_app = AIApp(
            name=name,
            description=description,
            icon=icon
        )
        db.add(ai_app)
        db.commit()
        db.refresh(ai_app)
        return ai_app 