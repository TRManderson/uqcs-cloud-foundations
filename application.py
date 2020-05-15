import flask
import sqlalchemy
import datetime
import waitress
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



ORMBase = declarative_base()

class Entry(ORMBase):
    __tablename__ = "entries"
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, primary_key=True)
    author = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)
    message = sqlalchemy.Column(sqlalchemy.Text)


app = flask.Flask(__name__)

Session = sessionmaker()

@app.route('/', methods=['POST'])
def add_new():
    try:
        data = flask.request.get_json()
        new_entry = Entry(
            message=data['message'],
            author=data['author'],
        )
        session = Session()
        session.add(new_entry)
        session.commit()
        session.close()
    except Exception as e:
        return flask.jsonify({
            'success': False,
            'message': repr(e)
            })
    return flask.jsonify({
        'success': True,
        **data
    })

@app.route('/', methods=['GET'])
def get_existing():
    session = Session()
    data = session.query(Entry).order_by(Entry.timestamp.desc()).limit(10).all()
    resp = flask.jsonify({'data': [
        {
            'timestamp': entry.timestamp.isoformat(),
            'message': entry.message,
            'author': entry.author
        }
        for entry in data
    ]})
    session.commit()
    session.close()
    return resp


def main():
    engine = sqlalchemy.create_engine(os.environ["DB_CONNECTION"])
    Session.configure(bind=engine)
    session = Session()
    ORMBase.metadata.create_all(session.connection())
    session.commit()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    waitress.serve(app, host=host, port=port, threads=1)


if __name__ == '__main__':
    main()

