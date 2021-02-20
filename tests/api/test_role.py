import json

from tests.api import APITest


class RoleTest(APITest):
    def test_create_role(self):
        response = self.client.post(
            '/api/v1/role/',
            data=json.dumps({'name': 'test'}),
            headers={'X-API-Key': self.key}
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json['name'], 'test')
        return True

    def test_get_role(self):
        response = self.client.post(
            '/api/v1/role/',
            data=json.dumps({'name': 'test'}),
            headers={'X-API-Key': self.key}
        )
        response = self.client.get(
            '/api/v1/role/%s' % response.json['id'],
            headers={'X-API-Key': self.key}
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json['name'], 'test')
        return True

    def test_edit_role(self):
        response = self.client.post(
            '/api/v1/role/',
            data=json.dumps({'name': 'test'}),
            headers={'X-API-Key': self.key}
            )
        self.assertEquals(response.status_code, 200)

        id = response.json['id']

        new_role = {
            'name': 'test2',
        }

        response = self.client.patch(
            '/api/v1/role/%s' % id,
            data=json.dumps(new_role),
            headers={'X-API-Key': self.key}
            )
        self.assertEquals(response.json['name'], 'test2')
        return True

    def test_delete_role(self):
        response = self.client.post(
            '/api/v1/role/',
            data=json.dumps({'name': 'test'}),
            headers={'X-API-Key': self.key}
        )

        self.assertEquals(response.status_code, 200)
        
        id = response.json['id']

        response = self.client.delete(
            '/api/v1/role/%s' % id,
            headers={'X-API-Key': self.key}
        )
        self.assertEquals(response.json['name'], 'test')
        response = self.client.get(
            '/api/v1/role/%s' % id,
            headers={'X-API-Key': self.key}
        )
        self.assertEquals(response.status_code, 404)
        return True
