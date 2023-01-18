import pandas as pd

def book_author(conn):
    return pd.read_sql('''SELECT * FROM book_author''',conn)

def change_book(conn,book,annot,note,id_type,id_book,part,year,closet,id_tag,id_author,link,old_author):
    cur = conn.cursor()
    cur.execute('''
        UPDATE book SET nameBook=:book,annotation=:annot,note=:note,ID_Type=:id_type WHERE ID_Book=:id_book;''',
                {"book":book,"annot":annot,"note":note,"id_type":id_type,"id_book":id_book})
    conn.commit()
    cur.execute('''UPDATE copy SET part=:part,releas=:year WHERE ID_Book=:id_book;''',
                {"part":part,"year":year,"id_book":id_book})
    conn.commit()
    cur.execute('''UPDATE storage SET closet=:closet,link=:link WHERE ID_Storage=(SELECT ID_Storage FROM copy WHERE ID_Book=:id_book);''',
                {"closet":closet,"id_book":id_book,"link":link})
    conn.commit()
    cur.execute('''UPDATE book_tag SET ID_Tag=:id_tag WHERE ID_Book=:id_book;''',
                {"id_tag":id_tag,"id_book":id_book})
    conn.commit()
    cur.execute('''UPDATE book_author SET ID_Author=:id_author WHERE ID_Author=:old AND ID_Book=:id_book;''',
                {"id_author":id_author,"id_book":id_book,"old":old_author})
    conn.commit()
    return True

def get_authors(conn):
    return pd.read_sql('''
    SELECT ID_Author,name FROM author
    ''',conn)

def get_type(conn):
    return pd.read_sql('''
    SELECT ID_Type,type FROM type
    ''',conn)

def get_tag(conn):
    return pd.read_sql('''
    SELECT ID_Tag,tag FROM tag
    ''',conn)

def get_old_author(conn,id_b):
    return pd.read_sql('''
    WITH get_authors(ID_Book,ID_Author, authors_name)
         AS (SELECT ID_Book,ID_Author, GROUP_CONCAT(name)
             FROM author
                      LEFT JOIN book_author USING (ID_Author)
             GROUP BY ID_Book),
        get_tag(ID_Book, ID_Tag, tag_book)
         AS (SELECT ID_Book,ID_Tag, tag
             FROM book_tag
                      LEFT JOIN tag USING (ID_Tag)
             GROUP BY ID_Book),
         get_storage(ID_Storage,link,mesto)
         AS (SELECT ID_Storage,link, closet || ' ' || shelf FROM storage)
                       
    SELECT 
    ID_Author AS 'Авторы'
    FROM book
        LEFT JOIN type USING (ID_Type)
        LEFT JOIN get_authors USING (ID_Book)
        LEFT JOIN get_tag USING (ID_Book)
        LEFT JOIN copy USING (ID_Book)
        LEFT JOIN get_storage USING (ID_Storage)
    WHERE ID_Book =:id_b; 
    ''',conn,params={"id_b":id_b})

def get_selected_book(conn,id):
    return pd.read_sql('''
    WITH get_authors(ID_Book,ID_Author, authors_name)
         AS (SELECT ID_Book,ID_Author, GROUP_CONCAT(name)
             FROM author
                      LEFT JOIN book_author USING (ID_Author)
             GROUP BY ID_Book),
        get_tag(ID_Book, ID_Tag, tag_book)
         AS (SELECT ID_Book,ID_Tag, tag
             FROM book_tag
                      LEFT JOIN tag USING (ID_Tag)
             GROUP BY ID_Book),
         get_storage(ID_Storage,link,mesto)
         AS (SELECT ID_Storage,link, closet || ' ' || shelf FROM storage)
                       
    SELECT ID_Book AS 'Номер',
    ID_Author AS 'Авторы',
    nameBook AS 'Название',
    part AS 'Том',
    year AS 'Год Издания',
    ID_Tag AS 'Тэг',
    ID_Type AS 'Тип',
    annotation AS 'Аннотация',
    note AS 'Заметки',
    mesto AS 'Расположение',
    link AS 'Ссылка'
    FROM book
        LEFT JOIN type USING (ID_Type)
        LEFT JOIN get_authors USING (ID_Book)
        LEFT JOIN get_tag USING (ID_Book)
        LEFT JOIN copy USING (ID_Book)
        LEFT JOIN get_storage USING (ID_Storage)
    WHERE ID_Book =:id_b; 
    ''',conn,params={"id_b":id})

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