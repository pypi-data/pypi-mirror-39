# Sqlalchemy bulk insert helper

A simple helper for bulk insert data with sqlalchemy



usage:

Let's assume we have a session and model

```python
from sqlalchemy import create_engine, INTEGER, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata
sess = sessionmaker(bind=create_engine("DB_URL"))()

class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(100))
```

create users  for simple which need to be inserted into db

```
users = [User(name=i) for i in ('Thor', 'Stark', 'Rogers', 'Scarlet Witch', 'Strange')]
```

And we can insert users with following code:

```python
from sa_insert_helper import bulk_insert

with bulk_insert(session=sess, model=User, n=1000) as bi:
    for u in users:
        bi.insert(u)
```

