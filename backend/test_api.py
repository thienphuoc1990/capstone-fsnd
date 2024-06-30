import os
from dotenv import load_dotenv
load_dotenv()

import unittest
import json
from src.api import create_app
from src.auth.auth import AuthError
from src.database.models import db, Actor, Movie
        
assistant_token = os.environ['CASTING_ASSISTANT_TOKEN']
director_token = os.environ['CASTING_DIRECTOR_TOKEN']
producer_token = os.environ['EXECUTIVE_PRODUCER_TOKEN']

class ApiTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.database_path = os.environ['DATABASE_TEST_PATH']

        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        self.seedData(self)

    @classmethod
    def tearDownClass(self):
        """Executed after reach test"""
        db.drop_all()
        pass

    def seedData(self):
        Actor(
            name="Christopher Robert Evans",
            age=43,
            gender="male"
        ).insert()
        Actor(
            name="Thomas Stanley Holland",
            age=28,
            gender="male"
        ).insert()
        Actor(
            name="Actor test delete",
            age=28,
            gender="male"
        ).insert()

        Movie(
            title="Captain America: The First Avenger",
            release_date="2011-07-29",
        ).insert()
        Movie(
            title="Marvel's Captain America: The Winter Soldier",
            release_date="2014-04-04",
        ).insert()
        Movie(
            title="Movie test delete",
            release_date="2014-04-04",
        ).insert()
    
    def getUserTokenHeaders(self, token=''):
        return { 'authorization': "Bearer " + token}     

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET /actors
    def test_get_actors(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/actors",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
            [{'age': 43, 'gender': 'male', 'id': 1, 'name': 'Christopher Robert Evans'}, 
             {'age': 28, 'gender': 'male', 'id': 2, 'name': 'Thomas Stanley Holland'}])
    
    # GET /actors/:id
    def test_get_actor_detail_success(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/actors/1", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
            {'age': 43, 'gender': 'male', 'id': 1, 'movies': [], 'name': 'Christopher Robert Evans'})
    
    def test_get_actor_detail_not_found(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/actors/100", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
    
    # POST /actors
    def test_post_actor_unauthorized(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().post("/actors", json={
            "name": "Scarlett Ingrid Johansson",
            "age": 39,
            "gender": "female",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'Permission denied')
        self.assertFalse(data["success"])
    
    def test_post_actor_unprocessable_entity(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().post("/actors", json={
            "name": "Christopher Robert Evans",
            "age": 43,
            "gender": "male"
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")
        
    def test_post_actor_success(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().post("/actors", json={
            "name": "Scarlett Ingrid Johansson",
            "age": 39,
            "gender": "female",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    # PATCH /actors
    def test_patch_actor_success(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().patch("/actors/1", json={
            "name": "Christopher Robert Evans",
            "age": 43,
            "gender": "male",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_patch_actor_unprocessable(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().patch("/actors/1", json={
            "name": "Thomas Stanley Holland",
            "age": 28,
            "gender": "male",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    # DELETE /actors/<int:id>
    def test_delete_actor_unauthorized(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().delete("/actors/1", headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'Permission denied')
        self.assertFalse(data["success"])

    def test_delete_actor_resource_not_found(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().delete("/actors/100", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actor_success(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().delete("/actors/3", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], 3)

    # GET /movies
    def test_get_movies_success(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/movies",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
            [{'id': 1, 'releaseDate': 'Fri, 29 Jul 2011 00:00:00 GMT', 'title': 'Captain America: The First Avenger'},
            {'id': 2, 'releaseDate': 'Fri, 04 Apr 2014 00:00:00 GMT', 'title': 'Marvel\'s Captain America: The Winter Soldier'}])
    
    # GET /movies/:id
    def test_get_movie_detail_success(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/movies/1", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
           {'actors': [], 'id': 1, 'releaseDate': 'Fri, 29 Jul 2011 00:00:00 GMT', 'title': 'Captain America: The First Avenger'})
    
    def test_get_movie_detail_fail(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/movies/100", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    # POST /movie
    def test_post_movie_unauthorized(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().post("/movies", json={
            "title": "Toy Story",
            "releaseDate": 'Wed, 22 Nov 1995 00:00:00 GMT',
        }, headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'Permission denied')
        self.assertFalse(data["success"])
        
    def test_post_movie_success(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().post("/movies", json={
            "title": "Toy Story",
            "releaseDate": 'Wed, 22 Nov 1995 00:00:00 GMT'
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    # PATCH /movie
    def test_patch_movie_unauthorized(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().patch("/movies/1", json={
            "title": "Captain America: The First Avenger 1",
            "releaseDate": 'Fri, 29 Jul 2011 00:00:00 GMT'
        }, headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'Permission denied')
        self.assertFalse(data["success"])

    def test_patch_movie_success_by_director(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().patch("/movies/1", json={
            "title": "Captain America: The First Avenger 1",
            "releaseDate": 'Fri, 29 Jul 2011 00:00:00 GMT'
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_patch_movie_success(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().patch("/movies/1", json={
            "title": "Captain America: The First Avenger 1",
            "releaseDate": 'Fri, 29 Jul 2011 00:00:00 GMT'
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_patch_movie_unprocessable(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().patch("/movies/1", json={
            "releaseDate": "Fri, 04 Apr 2014 00:00:00 GMT",
            "title": "Marvel's Captain America: The Winter Soldier"
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")
    
    
    # DELETE /movie/<int:question_id>
    def test_delete_movie_unauthorized(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().delete("/movies/1", headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'Permission denied')
        self.assertFalse(data["success"])

    def test_delete_movie_resource_not_found(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().delete("/movies/100", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie_success(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().delete("/movies/3", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], 3)

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()