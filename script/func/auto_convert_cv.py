# -*- coding: utf-8 -*-

from db_config import db_client
from cv_alias import alias

client = db_client()
works = client['onseidb']['meta']

def main():
    workList = list(works.find({}, ['id', 'cv', 'cv_alias']))
    for work in workList:
        if 'cv' in work.keys():
            cv_alias = []
            for cv in work['cv']:
                if cv in alias.keys():
                    cv = alias[cv]
                cv_alias.append(cv)
            cv_alias = list(set(cv_alias))
            if 'cv_alias' not in work.keys():
                works.update_one({'id': work['id']}, {'$set': {'cv_alias': cv_alias}})
            else:
                if set(work['cv_alias']) != set(cv_alias):
                    works.update_one({'id': work['id']}, {'$set': {'cv_alias': cv_alias}})

if __name__ == '__main__':
    main()
