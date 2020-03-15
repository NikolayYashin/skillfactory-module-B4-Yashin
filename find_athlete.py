# испортируем модули стандартнй библиотеки  datetime
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя    
    email = sa.Column(sa.Text)
    # день рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.INTEGER)

class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.INTEGER)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию

    return session()

def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    print()
    query = session.query(User).all()
    if  int(name) > len(query):
        print ("Пользователя с таки идентификатором нет, максимальный идентификатор позьдователя:", len(query))
        print()
        return
    quer=query[int(name)-1]
    # print(User)   
    print("Пользователь:            ", quer.id, quer.first_name, quer.last_name, quer.gender, quer.email, quer.birthdate, quer.height)

    query1 = session.query(Athelete).filter(Athelete.height > 0)
    # print(query1.count())
    myList=[]
    number_cnt = 0 
    for number in query1:
        myList.append(query1[number_cnt].height)
        number_cnt = number_cnt + 1
    myNumber = quer.height
    nea_height = (min(myList, key=lambda x:abs(x-myNumber)))
    # print (nea_height)
    query2 = session.query(Athelete).filter(Athelete.height == nea_height)
    print()
    print("Ближайший рост:          ", query2[0].id, query2[0].name, query2[0].gender, query2[0].birthdate, query2[0].height)

    query3 = session.query(Athelete).filter(Athelete.birthdate > 0)
    # print(query3.count())
    myList3=[]
    number_cnt = 0
    for number in query3:
        # date_list = query3[number_cnt].birthdate
        # date_list = datetime.datetime.strptime(date_list, "%Y-%m-%d")
        # print (date_list)
        date_list = query3[number_cnt].birthdate
        date_list = date_list.replace("-", "")
        date_list = int(date_list)
        myList3.append(date_list)
        number_cnt = number_cnt + 1
    # print (myList3)
    myNumber = quer.birthdate
    myNumber = int(myNumber.replace("-", ""))
    nea_birthdate = (min(myList3, key=lambda x:abs(x-myNumber)))
    nea_birthdate = str(nea_birthdate)
    nea_birthdate = nea_birthdate[0:4]+"-"+nea_birthdate[4:6]+"-"+nea_birthdate[6:8]
    query4 = session.query(Athelete).filter(Athelete.birthdate == nea_birthdate)
    print("Ближайший день рождения: ", query4[0].id, query4[0].name, query4[0].gender, query4[0].birthdate, query4[0].height)
    print()
    return


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    print()
    name_id = input("Введите идентификатор пользователя: ")
    # вызываем функцию поиска по имени
    # users_cnt, user_ids, log = find(name_id, session)
    find(name_id, session)

    # print (users_cnt, user_ids, log)

	# запрашиваем данные пользоватлея
    # user = request_data()
    # добавляем нового пользователя в сессию
    # session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо")


if __name__ == "__main__":
    main()