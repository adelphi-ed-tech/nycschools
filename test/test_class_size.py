from nycschools import class_size
import ssl

# Temporarily disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def test_get_class_size():
    df = class_size.get_class_size()
    cols = {'ay', 'dbn', 'grade', 'students_n', 'classes_n', 'avg_class_size',
            'min_class_size', 'max_class_size', 'dept', 'subject'}
    assert cols.issubset(df.columns)
    assert df.ay.nunique() >= 2


def test_load_class_size():
    df = class_size.load_class_size()

    cols = {'dbn', 'school_name', 'grade', 'program_type', 'students_n',
       'classes_n', 'avg_class_size', 'min_class_size', 'max_class_size',
       'dept', 'subject', 'ay'}
    assert cols.issubset(df.columns)
    assert df.ay.nunique() >= 2

def test_load_ptr():
    df = class_size.load_ptr()
    cols = {'dbn', 'school_name', 'ptr', 'ay'}
    assert cols.issubset(df.columns)

