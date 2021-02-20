import json

from tests.api import APITest


class UserTest(APITest):
    def test_create_user(self):
        response = self.client.post(
            '/api/v1/user/',
            data=json.dumps(
                {
                    'username': 'test2',
                    'password': 'test',
                    'role_names': ['admin', 'user']
                }
            ),
            headers={'X-API-Key': self.key}
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.json['username'], 'test2')
        self.assertEquals(response.json['is_active'], False)
        self.assertTrue(len(response.json['api_key']) == 64)
        self.assertEquals(self.strp_strf(response.json['created']), response.json['created'])
        return True

    def test_get_user(self):
        response = self.client.post(
            '/api/v1/user/',
            data=json.dumps(
                {
                    'username': 'test2',
                    'password': 'test',
                    'role_names': ['admin', 'user']
                }
            ),
            headers={'X-API-Key': self.key}
        )

        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(
            '/api/v1/user/%s' % response.json['id'],
            headers={'X-API-Key': self.key}
        )

        self.assertEquals(response.json['username'], 'test2')
        self.assertEquals(response.json['is_active'], False)
        self.assertTrue(len(response.json['api_key']) == 64)
        self.assertEquals(self.strp_strf(response.json['created']), response.json['created'])
        
        return True

    def test_edit_user(self):
        response = self.client.post(
            '/api/v1/user/',
            data=json.dumps(
                {
                    'username': 'test2',
                    'password': 'test',
                    'role_names': ['admin', 'user']
                }
            ),
            headers={'X-API-Key': self.key}
        )

        self.assertEquals(response.status_code, 200)

        new_user = {
            'username': 'test3',
            'is_active': True
        }

        response = self.client.patch(
            '/api/v1/user/%s' % response.json['id'],
            data=json.dumps(new_user),
            headers={'X-API-Key': self.key}
            )
        self.assertEquals(response.json['username'], 'test3')
        self.assertEquals(response.json['is_active'], True)
        return True

    def test_delete_user(self):
        response = self.client.post(
            '/api/v1/user/',
            data=json.dumps(
                {
                    'username': 'test2',
                    'password': 'test',
                    'role_names': ['admin', 'user']
                }
            ),
            headers={'X-API-Key': self.key}
        )

        self.assertEquals(response.status_code, 200)

        response = self.client.delete(
            '/api/v1/user/%s' % response.json['id'],
            headers={'X-API-Key': self.key}
        )

        response = self.client.get(
            '/api/v1/user/%s' % response.json['id'],
            headers={'X-API-Key': self.key}
        )
        self.assertEquals(response.status_code, 404)
        return True
