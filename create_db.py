from app import app, db
from models import Song, Artist, Album

with app.app_context():
    db.create_all()

    # создаем тестовых исполнителей
    artist1 = Artist(name='The Rasmus')
    artist2 = Artist(name='Канцлер Ги')
    artist3 = Artist(name='CHVRCHES')
    db.session.add_all([artist1, artist2, artist3])
    db.session.commit()

    # создаем тестовые альбомы
    album1 = Album(title='Dead Letters', year='2003', artist=artist1)
    album2 = Album(title='Black Roses', year='2008', artist=artist1)
    album3 = Album(title='Лирика', year='2017', artist=artist2)
    album4 = Album(title='Love Is Dead', year='2018', artist=artist3)
    album5 = Album(title='Screen', year='Violence', artist=artist3)

    # создаем тестовые песни
    song1 = Song(title='First Day Of My Life', length='3:44', track_number=1, album=album1)
    song2 = Song(title='Livin In A World Without You', length='3:50', track_number=1, album=album2)
    song3 = Song(title='Мадонна канцлера Ролена', length='3:58', track_number=13, album=album3)
    song4 = Song(title='Miracle', length='3:08', track_number=7, album=album4)
    song5 = Song(title='Nightmares', length='4:33', track_number=9, album=album5)

    db.session.add_all([album1, album2, album3, album4, album5, song1, song2, song3, song4, song5])
    db.session.commit()