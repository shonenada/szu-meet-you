from sqlalchemy.orm import Session

from szumu.message.model import Message
from szumu.user.model import User


session = Session()
query = session.query(Message)


def remove_msg(msg):
    if isinstance(msg, Message):
        session.delete(msg)
        session.commit()
        return True
    else:
        return False


def save_msg(msg):
    if isinstance(msg, Message):
        session.add(msg)
        session.commit()
        return True
    else:
        return False


def check_new_msg(to_id):
    count = (query.filter(Message.toid == to_id)
                  .filter(Message.state == Message.NOT_READED)
                  .filter(Message.to_hide == 0)
                  .count())
    if count > 0:
        return True
    else:
        return False


def set_all_readed(user_id):
    msgs = query.filter_by(toid=user_id).all()
    for msg in msgs:
        msg.state = Message.READED
    session.commit()


def get_ones_receive_msg(user_id):
    if user_id is None:
        return None
    else:
        msgs = (query.filter(Message.toid == user_id)
                     .filter(Message.to_hide == 0).all())
        return msgs


def get_ones_send_msg(user_id):
    if user_id is None:
        return None
    else:
        msgs = (query.filter(Message.fromid == user_id)
                     .filter(Message.from_hide == 0).all())
        return msgs


def find(msg_id):
    if msg_id is None:
        return None
    else:
        msg = query.filter_by(id=msg_id).first()
        return msg