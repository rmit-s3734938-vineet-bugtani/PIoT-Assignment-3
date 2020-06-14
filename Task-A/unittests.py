import unittest
import flask
from flask import request
import requests, json
from passlib.hash import sha256_crypt
from json import JSONEncoder
import datetime
from datetime import date, time
import voice_search


class TestStringMethods(unittest.TestCase):
    # Will change depending on which device the code is run
    BASE_URL = "http://192.168.1.225:5000"
    INCORRECT_USERNAME = "mWoodss"

    # Tests for "/engineer/<username>" - API to get engineer profile by username
    def test_engineer_inCorrectUsername(self):
        response = requests.post(self.BASE_URL+"/engineer/"+self.INCORRECT_USERNAME)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid engineer username")
        self.assertEqual(response.status_code, 404)

    # Tests for "/reportFaults" - API to assign faulty cars
    def test_reportFaults_notSupplyingUsername(self):
        data = {"carIds":[1,2]}
        response = requests.post(self.BASE_URL+"/reportFaults", json=data)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Engineer username not supplied")
        self.assertEqual(response.status_code, 400)
    
    def test_reportFaults_notSupplyingCarIds(self):
        data = {"engineerName":"mWoods"}
        response = requests.post(self.BASE_URL+"/reportFaults", json=data)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "No car ids supplied")
        self.assertEqual(response.status_code, 400)
    
    def test_reportFaults_inCorrectUsername(self):
        data = {"engineerName":self.INCORRECT_USERNAME,"carIds":[1,2]}
        response = requests.post(self.BASE_URL+"/reportFaults", json=data)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid engineer username")
        self.assertEqual(response.status_code, 404)

    # Tests for "/loginUser" - API to login user
    def test_login_correctUsernameAndPassword(self):
        userLoginData = {"username":"s3734938", "password":"password"}
        response = requests.post(self.BASE_URL+"/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Success")
        self.assertEqual(response.status_code, 200)

    def test_login_correctUsernameAndIncorrectPassword(self):
        userLoginData = {"username":"s3734938", "password":"passwordTrial"}
        response = requests.post(self.BASE_URL+"/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
        self.assertEqual(response.status_code, 404)
    
    def test_login_inCorrectUsernameAndCorrectPassword(self):
        userLoginData = {"username":self.INCORRECT_USERNAME, "password":"password"}
        response = requests.post(self.BASE_URL+"/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
        self.assertEqual(response.status_code, 404)
    
    def test_login_inCorrectUsernameAndPassword(self):
        userLoginData = {"username":self.INCORRECT_USERNAME, "password":"passwordp"}
        response = requests.post(self.BASE_URL+"/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
        self.assertEqual(response.status_code, 404)
    
    def test_login_notSupplyingUsername(self):
        userLoginData = {"password":"passwordp"}
        response = requests.post(self.BASE_URL+"/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Username not supplied")
        self.assertEqual(response.status_code, 400)
    
    def test_login_notSupplyingPassword(self):
        userLoginData = {"username":"s3734932"}
        response = requests.post(self.BASE_URL+"/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Password not supplied")
        self.assertEqual(response.status_code, 400)
    
    def test_audio_one(self):
        text = voice_search.start_recognition("audio/1.flac")
        self.assertEqual(text, "Alto")
    
    def test_audio_two(self):
        text = voice_search.start_recognition("audio/2.flac")
        self.assertEqual(text, "black")
    
    def test_audio_three(self):
        text = voice_search.start_recognition("audio/3.flac")
        self.assertEqual(text, "blue")

    def test_audio_four(self):
        text = voice_search.start_recognition("audio/4.flac")
        self.assertEqual(text, "Civic")
    
    def test_audio_five(self):
        text = voice_search.start_recognition("audio/5.flac")
        self.assertEqual(text, "Red and black honda sedan")
    
    def test_audio_six(self):
        text = voice_search.start_recognition("audio/6.flac")
        self.assertEqual(text, "Red honda")
    

if __name__ == "__main__":
    unittest.main()    