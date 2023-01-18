import pandas as pd


def get_books(con):
    return pd.read_sql('''

     WITH get_authors(ID_Book, authors_name)
         AS (SELECT ID_Book, GROUP_CONCAT(name)
             FROM author
                      JOIN book_author USING (ID_Author)
             GROUP BY ID_Book),
        get_tag(ID_Book, tag_book)
         AS (SELECT ID_Book, tag
             FROM book_tag
                      JOIN tag USING (ID_Tag)
             GROUP BY ID_Book)

    SELECT ID_Book AS 'Номер',
    authors_name AS 'Авторы',
    nameBook AS 'Название',
    part AS 'Том',
    year AS 'Год Издания',
    tag_book AS 'Тэг',
    type AS 'Тип'
    FROM book
        LEFT JOIN type USING (ID_Type)
        LEFT JOIN get_authors USING (ID_Book)
        LEFT JOIN get_tag USING (ID_Book)
        LEFT JOIN copy USING (ID_Book)
    ORDER BY ID_Book 
    ''', con)

#_________________Для списков_____________
def get_tags(con):
    return pd.read_sql(
        '''SELECT * FROM tag
''', con)

def get_types(con):
    return pd.read_sql(
        '''SELECT * FROM type
''', con)

#_______________Добавить книгу____________
def get_new_book(con, new_name, new_annot, new_note, new_type):
    cur = con.cursor()

    cur.execute('''
INSERT INTO book(nameBook, annotation, note, ID_Type) VALUES (:new_name, :new_annot, :new_note, :new_type)
    ''', {"new_name": new_name, "new_annot": new_annot, "new_note": new_note, "new_type": new_type})

    con.commit()

    return cur.lastrowid


def get_new_author(con, new_author):
    cur = con.cursor()

    cur.execute('''
    INSERT INTO author(name) Values (:new_author)

    ''', {"new_author": new_author})
    con.commit()
    return cur.lastrowid


def get_new_book_author(con, new_id_book, new_id_author):
    cur = con.cursor()

    cur.execute('''
        INSERT INTO book_author(ID_Author,ID_Book) Values (:new_id_author,:new_id_book)

        ''', {"new_id_author": new_id_author, "new_id_book": new_id_book})
    con.commit()
    return cur.lastrowid


def gen_new_storage(con, new_closet, new_shelf, new_link):
    cur = con.cursor()

    cur.execute('''
            INSERT INTO storage(closet,shelf,link) Values (:new_closet,:new_shelf, :new_link )

            ''', {"new_closet": new_closet, "new_shelf": new_shelf, "new_link": new_link})
    con.commit()
    return cur.lastrowid


def gen_new_copy(con, new_year, new_part, new_book, new_storage):
    cur = con.cursor()

    cur.execute('''
            INSERT INTO copy(year,part,ID_Book,ID_Storage) Values (:new_year,:new_part, :new_book, :new_storage )

            ''', {"new_year": new_year, "new_part": new_part, "new_book": new_book, "new_storage": new_storage})
    con.commit()
    return cur.lastrowid


def gen_new_book_tag(con, new_tag, new_book):
    cur = con.cursor()

    cur.execute('''
            INSERT INTO book_tag(ID_Tag,ID_Book) Values (:new_tag,:new_book)

            ''', {"new_tag": new_tag, "new_book": new_book})
    con.commit()
    return cur.lastrowid

#_____________________________________________________
#_______Поиск________
def get_authors(con):
    return pd.read_sql(
        '''SELECT * FROM author
''', con)


def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = ",".join(s)

    return res


def search(con, aut, t, typ):

    return pd.read_sql(f'''
     WITH get_authors(ID_Book, authors_name,ID_Author)
         AS (SELECT ID_Book, GROUP_CONCAT(name),ID_Author
             FROM author
                      JOIN book_author USING (ID_Author)
             GROUP BY ID_Book),
        get_tag(ID_Book, tag_book,ID_Tag)
         AS (SELECT ID_Book, tag,ID_Tag
             FROM book_tag
                      JOIN tag USING (ID_Tag)
             GROUP BY ID_Book)

    SELECT ID_Book AS 'Номер',
    authors_name AS 'Авторы',
    nameBook AS 'Название',
    part AS 'Том',
    year AS 'Год Издания',
    tag_book AS 'Тэг',
    type AS 'Тип'
    FROM book
        LEFT JOIN get_tag USING (ID_Book)
        LEFT JOIN get_authors USING (ID_Book)
        LEFT JOIN type USING (ID_Type)
        LEFT JOIN copy USING (ID_Book)
    GROUP BY ID_Book
    HAVING  (ID_Author IN ({aut}) OR ({not aut}))
             AND (ID_Type IN ({typ}) OR ({not typ}))
             AND (ID_Tag IN ({t}) OR ({not t}))

    ORDER BY
            ID_Book
    ''', con)
