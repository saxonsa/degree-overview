import unittest
from app import app
import json


class TestLogin(unittest.TestCase):
    """
        Define the test case
    """

    def setUp(self) -> None:
        """
            It is called before the specific test method is executed.
        """
        self.app = app

        # Activation test flag
        app.config['TESTING'] = True
        # Here, the test is performed using the test client provided by flask
        self.client = app.test_client()

    def test_empty_userid_or_password_or_role(self):
        """ Test empty name or password """

        response = self.client.post("/user/login?")
        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # assert if the code in the dict
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # Test only receive userId
        response = self.client.post("/user/login?userId=1830026097")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "Error! Missing parameters")

        # Test only receive password
        response = self.client.post("/user/login?password=123")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "Error! Missing parameters")

        # test only receive role
        response = self.client.post("/user/login?role=student")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "Error! Missing parameters")

        # Test only receive userId and password
        response = self.client.post("/user/login?userId=1830026097&password=123")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "Error! Missing parameters")

        # Test only receive userId and role
        response = self.client.post("/user/login?userId=1830026097&role=student")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "Error! Missing parameters")

        # Test only receive user id and role
        response = self.client.post("/user/login?userId=123&role=student")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3001
        code = resp_dict.get("code")
        self.assertEqual(code, 3001)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "Error! Missing parameters")

    def test_not_exist_user(self) -> None:
        """ Test not exist user """

        # e.g. student with 111 does not exist
        response = self.client.post("/user/login?userId=111&password=123&role=student")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 3002)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "No such user found, please check the username or the selected role")

        # e.g. lecturer with 111 does not exist
        response = self.client.post("/user/login?userId=111&password=123&role=lecturer")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 3002)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "No such user found, please check the username or the selected role")

        # e.g. lecturer with 111 does not exist
        response = self.client.post("/user/login?userId=111&password=123&role=designer")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 3002)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "No such user found, please check the username or the selected role")

        # e.g. User 1830026097 is a student
        response = self.client.post("/user/login?userId=1830026097&password=123&role=designer")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 3002)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "No such user found, please check the username or the selected role")

    def test_wrong_password(self) -> None:
        # e.g. Correct password for 1830026097 is 123
        response = self.client.post("/user/login?userId=1830026097&password=1234&role=student")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3003
        code = resp_dict.get("code")
        self.assertEqual(code, 3003)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "wrong password")

        # e.g. Correct password for ninama is 123
        response = self.client.post("/user/login?userId=ninama&password=1234&role=lecturer")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3003
        code = resp_dict.get("code")
        self.assertEqual(code, 3003)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "wrong password")

        # e.g. Correct password for judyfeng is 123
        response = self.client.post("/user/login?userId=judyfeng&password=1234&role=designer")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3003
        code = resp_dict.get("code")
        self.assertEqual(code, 3003)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "wrong password")

    def test_correct_name_password(self) -> None:
        # e.g. correct student
        response = self.client.post("/user/login?userId=1830026097&password=123&role=student")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 200)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "success")

        # return result
        result = resp_dict.get('result')
        self.assertEqual(result['me'], {
            'email': 'n830026097@mail.uic.edu.cn',
             'engname': 'Saxon',
             'gender': 'Male',
             'nickname': 'Xingyun SA',
             'phone': '15206902190',
             'program': 'CST',
             'role': 'student'}
        )

        # correct lecturer
        response = self.client.post("/user/login?userId=ninama&password=123&role=lecturer")

        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 200)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "success")

        # return result
        result = resp_dict.get('result')
        self.assertEqual(result['me'], {
            "designAuth": 0,
            "email": "nina@mail.uic.edu.cn",
            "engname": "Nina",
            "gender": "Female",
            "nickname": "Yingran MA",
            "phone": "1111",
            "program": "CST",
            "role": "lecturer"
        })

        # correct designer
        response = self.client.post("/user/login?userId=judyfeng&password=123&role=designer")


        # response data
        resp_json = response.data

        # convert to json
        resp_dict = json.loads(resp_json)

        # use assert to verify
        self.assertIn("code", resp_dict)

        # compare the code value 3002
        code = resp_dict.get("code")
        self.assertEqual(code, 200)

        # return info
        info = resp_dict.get('info')
        self.assertEqual(info, "success")

        result = resp_dict.get('result')
        self.assertEqual(result['me'], {
            "designAuth": 1,
            "email": "xinfeng@mail.uic.edu.cn",
            "engname": "Judy",
            "gender": "Female",
            "nickname": "Xin Feng",
            "phone": "1111131",
            "program": "CST",
            "role": "designer"
        })



if __name__ == '__main__':
    unittest.main()
