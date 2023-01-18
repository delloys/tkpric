from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import *
import pandas as pd


@app.route('/index', methods=['get', 'post'])
def index():
    con = get_db_connection()

    book_name = ''
    author = -1
    tom = ''
    year = -1
    desc = ''
    annot = ''
    id_book=-1
    type=-1
    rasp=''
    tag=-1
    link=''
    old_author=-1

    if request.values.get('id_book'):
        id_book = request.values.get('id_book')

    if request.values.get('confirm'):
        book_name = request.values.get('new_name')
        author = request.values.get('new_authors')
        tom = request.values.get('new_tom')
        year = request.values.get('new_year')
        count_book = request.values.get('new_kol_vo')
        desc = request.values.get('new_desc')
        annot = request.values.get('new_annot')
        type = request.values.get('type')
        tag = request.values.get('tag')
        rasp = request.values.get('new_rasp')
        link = request.values.get('new_link')
        old_author = request.values.get('old_author')
        df_change_bok = change_book(con, book_name, annot, desc, type, id_book, tom, int(year), rasp, tag, int(author), link,int(old_author))


    df_old_author = get_old_author(con,id_book)
    df_books = get_books(con)
    df_select_book = get_selected_book(con, id_book)
    df_tag = get_tag(con)
    df_type = get_type(con)
    df_author = get_authors(con)

    html = render_template(
        'index.html',
        id_book = id_book,
        books = df_books,
        select_book = df_select_book,
        tags = df_tag,
        types = df_type,
        authors = df_author,
        old_author = df_old_author,
        len=len,
        int = int
        )

    return html