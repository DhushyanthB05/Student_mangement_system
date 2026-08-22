from app import create_app
from app.extensions import db
from app.models.models import User, Department, Course

app = create_app()

@app.cli.command("init-db")
def init_db():
    "Initialize the database."
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create an initial admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            
        # Create Dummy Departments and Courses
        cs = Department(name="Computer Science", code="CS")
        it = Department(name="Information Technology", code="IT")
        db.session.add_all([cs, it])
        db.session.commit()
        
        c1 = Course(name="B.Tech Computer Science", code="BTECH-CS", department_id=cs.id)
        c2 = Course(name="M.Tech Computer Science", code="MTECH-CS", department_id=cs.id)
        c3 = Course(name="B.Tech Info Tech", code="BTECH-IT", department_id=it.id)
        db.session.add_all([c1, c2, c3])
        db.session.commit()
        
        print('Initialized database, created admin user, and populated dummy departments/courses')

if __name__ == '__main__':
    app.run(debug=True)
