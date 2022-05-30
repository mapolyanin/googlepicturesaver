from googlepicturesaver.googlepicturesaver import Validator
LONG_STRING = """Из-за такой повышенной гибкости динамически типизированные языки уступают статически 
                 типизированным в скорости во время выполнения. Требуется провести множество проверок 
                 на определение типов переменных и других конструкций, чтобы обеспечить работу программы. 
                 А все это создает дополнительную нагрузку. В настоящее время Python является приоритетным 
                 языком для машинного обучения и все чаще используется для разработки 
                 API и веб-приложений, обслуживающих модели МО. 
                 Намного проще создавать модели и обертывать их в ориентированное на 
                 пользователя приложение с помощью одного языка, чем нескольких."""
print(LONG_STRING)
print(len(LONG_STRING))
print(len(LONG_STRING.split()))

def test_validate_query_string(test):
    validator = Validator(test)
    print("Начало:")
    print(validator.validate_query_string())
    print(validator.query_string)
    print('Путь:')
    print(validator.path_string, "!")


    """ 
    validator.correct_query = True
    validator.validate_query_string('')
    assert validator.correct_query == False

    validator.__init__()
    assert validator.correct_query == False
    assert validator.correct_path == False

    validator.correct_query = True
    validator.validate_query_string('')
    """
test_validate_query_string(LONG_STRING)

test_validate_query_string(" # дорогая редакция")