from googlepicturesaver.googlepicturesaver import GoogleEngine

LONG_STRING = """Из-за такой повышенной гибкости динамически типизированные языки уступают статически 
                 типизированным в скорости во время выполнения. Требуется провести множество проверок 
                 на определение типов переменных и других конструкций, чтобы обеспечить работу программы. 
                 А все это создает дополнительную нагрузку. В настоящее время Python является приоритетным 
                 языком для машинного обучения и все чаще используется для разработки 
                 API и веб-приложений, обслуживающих модели МО. 
                 Намного проще создавать модели и обертывать их в ориентированное на 
                 пользователя приложение с помощью одного языка, чем нескольких."""

def test_googleengine_get_search_page():
    google_engine = GoogleEngine()
    google_engine.get_search_page('корова')
    assert google_engine.successful_request == True
    google_engine.parse_links()
    assert len(google_engine.file_links) != 0
    google_engine.download_files()
    assert len(google_engine.files) != 0
    google_engine.get_search_page(LONG_STRING)
    print(google_engine.answer.status_code)
    with open('page.html', 'w') as f:
        f.write(google_engine.answer.text)


test_googleengine_get_search_page()
