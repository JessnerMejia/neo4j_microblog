from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
from datetime import datetime
from pandas import DataFrame
import os
import uuid


passwd = "your_password"

url='http://localhost:7474'
graph = Graph(url + '/db/data/', password=passwd)


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        # matcher = NodeMatcher(graph)
        # user = matcher.match('User', username=self.username).first()
        user_q='''MATCH (u:User) WHERE u.username="{}" RETURN u'''.format(self.username)
        user = graph.run(user_q).evaluate()
        return user

    def register(self, password):
        if not self.find():
            print("entro")
            user = Node('User', username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        usuario = self.find()
        print(usuario['password'])
        print(password)
        if usuario:
            if bcrypt.verify(password, usuario['password']):
                return True
        else:
            return False

    def add_post(self, title, tags, text):
        tx = graph.begin()
        user = self.find()
        post = Node(
            'Post',
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, "PUBLISHED", post)
        tx.create(rel)
        tx.commit()

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tx_1 = graph.begin()
            tag = Node('Tag', name=name)
            rela = Relationship(tag, "TAGGED", post)
            tx_1.create(rela)
            tx_1.commit()


    def like_post(self, post_id):
        user = self.find()
        #post = graph.find_one('Post', 'id', post_id)
        statement = '''MATCH (n:Post) WHERE (n.id="{}") RETURN n,labels(n)''' .format(post_id)
        post = graph.run(statement).evaluate()
        #MATCH (n:Post) WHERE (n.id="575a7060-4ce6-47f7-a5ee-b263e56d3337") RETURN n,labels(n)
        graph.merge(Relationship(user, 'LIKED', post))

    def get_recent_posts(self):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = "{}"
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        '''.format(self.username)
        resultado_q=graph.run(query)

        return resultado_q

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = '''
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = "{}" AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''.format(self.username)

        return graph.run(query)

    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = '''
        MATCH (they:User {{ username: "{}" }})
        MATCH (you:User {{ username: "{}" }})
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN SIZE((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
               COLLECT(DISTINCT tag.name) AS tags
        '''.format(other.username,self.username)
        usuario_com = graph.run(query).evaluate()

        return usuario_com

def get_todays_recent_posts():
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = "{}"
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''.format(date())

    return graph.run(query)

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')
