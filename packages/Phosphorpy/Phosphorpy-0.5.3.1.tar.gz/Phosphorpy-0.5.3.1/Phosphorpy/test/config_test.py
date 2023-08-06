from SearchEngine.config.config import SearchConfig
from SearchEngine.config.survey_data import read_survey_data
import configparser
import os


def test_config_parser():
    conf = configparser.ConfigParser()
    print(os.path.abspath('../local/'))
    conf.read('../local/survey.conf')
    print(conf.sections())
    print(conf['survey1']['columns'].split(', '))


def test_config_reader():
    print(read_survey_data())


def test_search_config1():
    sc = SearchConfig('./search_files/search_test1.conf')
    print()
    # print(sc.commands.sections())
    # print(dict(sc.commands.items('query1')))

    sc.start()
